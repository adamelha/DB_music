(function () {
    'use strict';

    angular.module('BlurAdmin')
        .directive('smartTable', smartTable);

    /** @ngInject */
    function smartTable() {
        return {
            restrict: 'EA',
            transclude: {
                'buttons': '?buttons',
            },
            templateUrl: 'app/directives/smart-table/smart-table.html',
            scope: {
                panelTitle: '=', // panel title
                pageSize: '=?',  // number of rows per page. options: [5,10,15,20,25]. (show all if undefined)
                // data: '=',       // table row data. structure: data{data: fieldsObject}
                leftColumn: '=?',  //table left column, pass with name(column name) and array of buttons// each button contains icon , onClick function , and isShownOnRow function
                rightColumn: '=?',
                rowButton: '=?',   // row onClick function
                setOfFunctionsFields: '=?', //generic form type: select
                editEnable: '=?', //if true, each data is editable
                editableColumns: '=?', //
                searchEnable: '=?', // if true, search for each column is enabled
                searchGlobal: '=?', // if true, global table search is enabled
                setOfFiltersFields: '=?',
                // languageId: '=',
                mockItems: '=?',
                tableConfig: '=' // {path,options,postProcess,fields,languageId} - path for call, options: same as rest-service, postProcess is a function that is called on results from server
            },
            controller: function ($scope, $transclude, editableOptions, editableThemes, $timeout, ServerConnection, $q) {
                $scope.tableState = {
                    items: [],
                    pageSize: 10,
                    page: 1
                };
                $scope.fields = $scope.tableConfig.fields;

                // if ($scope.tableConfig.setDataManually) {
                //     $scope.tableConfig.setDataManually = function (items) {
                //         $scope.tableState.items = items;
                //         $timeout(() => $scope.$apply(), 0);
                //     }
                // }

                function setFieldDisplayValue(fields, fieldName, value) {
                    let f = fields.filter((f) => f.name == fieldName)[0]
                    f.displayedValue = value;
                }

                $scope.setFieldDisplayValue = setFieldDisplayValue;


                function getFieldByPath(object, path) {
                    var a = path.split('.');
                    var o = object;
                    for (var i = 0; i < a.length - 1; i++) {
                        var n = a[i];
                        if (n in o) {
                            o = o[n];
                        } else {
                            o[n] = {};
                            o = o[n];
                        }
                    }
                    return o[a[a.length - 1]];
                }

                $scope.getFieldByPath = getFieldByPath;
                editableOptions.theme = 'bs3';
                editableThemes['bs3'].submitTpl = '<button type="submit" class="btn btn-primary btn-with-icon"><i class="ion-checkmark-round"></i></button>';
                editableThemes['bs3'].cancelTpl = '<button type="button" ng-click="$form.$cancel()" class="btn btn-default btn-with-icon"><i class="ion-close-round"></i></button>';


                $scope.isButtonsTranscludePresent = () => {
                    return $transclude.isSlotFilled('buttons');
                };

                //

                $scope.isColumnEditable = colIndex => {
                    return !(!$scope.editEnable || $scope.fields[colIndex].readOnly);
                };

                $scope.rowButtonClicked = item => {
                    if ($scope.rowButton) {
                        $scope.rowButton.onClick(item);
                    }
                };

                $scope.getFieldValue = function (item, field) {
                    if (field.multiLanguage && $scope.languageId) {
                        let tran = item.translations.filter(tran => tran.languageId == $scope.languageId)[0];
                        return tran && tran.texts ? tran.texts[field.name] : null;
                    }

                    let retVal;
                    let val = $scope.getFieldByPath(item, field.name);
                    switch (field.type) {
                        case 'multiSelect':
                            retVal = val ? val.map(val => field.options.filter(option => option.key == val)[0].value).join(', ') : '';
                            break;
                        default:
                            retVal = `${val ? val : '-'} ${field.suffix || ''}`;
                    }

                    return retVal;

                }


                $scope.addCheckedItemToList = index => {
                    $scope.setOfFunctionsFields.checkMarkList.push(index)
                };

                $scope.hiddenFilter = field => !field.tableHidden;

                $scope.toggleFieldFilter = (field, $event) => {
                    field.filter = field.filter || {};
                    field.filter.open = !field.filter.open;
                    $event.stopPropagation();
                }

                $scope.stopProp = ($event) => {
                    $event.stopPropagation();
                }

                //called whenever a change is made in table state, tableCtrl:{pagination,sort,search}
                $scope.getDataFromServer = function (tableCtrl, a, field) {


                    $scope.tableState.isLoading = true;
                    tableCtrl.filter = tableCtrl.filter || {};
                    updateFilter(tableCtrl, field)
                    $scope.tableCtrl = tableCtrl;
                    $scope.tableState.pageSize = tableCtrl.pagination.number;
                    //
                    // //set options for server call by current table state
                    let paging = getPagination(tableCtrl.pagination)
                    let sort = getSort(tableCtrl.sort)
                    let filters = Object.assign({}, $scope.tableConfig.options.filter, tableCtrl.filter)
                    let populate = $scope.tableConfig.options.populate;
                    let reqOtions = {filters, paging, sort, populate}
                    //
                    let reqResult;
                    if ($scope.mockItems) {
                        reqResult = returnMock();
                    }
                    else{
                        reqResult = ( ServerConnection.get($scope.tableConfig.path, reqOtions))

                    }
                    reqResult.then((res)=>{
                        $scope.tableState.items = res.results;
                        let items = res.results;
                        let itemCount = reqResult.total_rows;
                        //
                        // //call post process function if there is one
                        if ($scope.tableConfig.postProcess) {
                            items = $scope.tableConfig.postProcess(items)
                        }
                        //
                        tableCtrl.pagination.numberOfPages = Math.ceil(itemCount / tableCtrl.pagination.number);
                        //
                        $scope.tableState.items = items;
                        //
                        $scope.tableState.isLoading = false;
                        //
                        $timeout(() => $scope.$apply(), 0);

                    })
                    //

                    return reqResult.promise;
                }

                function returnMock() {
                    let d = $q.defer();
                    $timeout(() => {
                        let items = $scope.mockItems || [];
                        d.resolve({total_rows:items.length, results:items})
                    });
                    return d.promise;
                }

                function updateFilter(tableCtrl, field) {
                    // tableCtrl.filter = Object.assign(tableCtrl.filter, getFieldFilter(field))

                    if (!field || !field.filter) return {};
                    if ((field.filter.value === -1 || field.filter.value === "" || field.filter.value === null)) {
                        delete tableCtrl.filter[field.name];
                    }
                    else {
                        switch (field.type) {
                            case 'select':
                                tableCtrl.filter[field.name] = field.filter.options.filter(op => {
                                    return op.key == field.filter.value
                                })[0].value;
                                break;
                            case 'boolean':
                                tableCtrl.filter[field.name] = $scope.booleanFilterOptions.filter(op => {
                                    return op.key == field.filter.value
                                })[0].key;
                                break;
                            case 'date': //TODO if needed, change format to YYYY-MM-DD
                                let {from, to} = field.filter.value;
                                tableCtrl.filter[field.name] = {'$and': {}};
                                tableCtrl.filter[field.name]['$and']['$>'] = field.filter.value.from;
                                tableCtrl.filter[field.name]['$and']['$<'] = field.filter.value.to;

                                break;
                            case 'number':
                                tableCtrl.filter[field.name] = field.filter.value;
                                break;
                            default: //text
                                tableCtrl.filter[field.name] = {'$like': field.filter.value};
                        }
                    }
                    // let filter = {}

                }

                function getSort(filter) {
                    return filter.predicate ? {field: filter.predicate, order: filter.reverse ? 'des' : 'asc'} : {}
                }

                function getPagination(filter) {
                    return {page: filter.start / filter.number + 1, pageSize: filter.number}
                }
            },
        };
    }

})();