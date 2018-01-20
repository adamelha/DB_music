(function () {
    'use strict';

    angular.module('BlurAdmin.additionalInfoModal',[])
        .directive('additionalInfoModal', additionalInfoModal);

    /** @ngInject */
    function additionalInfoModal() {
        return {
            restrict: 'A',
            scope: {
                info: '='
            },
            controller: ['$scope', '$uibModal', '$q',
                function ($scope, $uibModal) {
                    this.openModal = function () {
                        return $uibModal.open(this.modalArgs())
                    };

                    this.modalArgs = function () {
                        return {
                            animation: true,
                            templateUrl: 'app/directives/additinal-info-modal/index.html',
                            size: 'md',
                            scope: $scope
                        }
                    };

                    $scope.bodyFrom = function (body) {
                        return JSON.stringify(body)
                    };

                    $scope.titleFrom = function (title) {
                        return title + ''
                    }
                }],
            link: function (scope, element, attrs, modalCtrl) {
                scope.state = scope.state || 'closed';

                function open() {
                    scope.state = 'open';
                    return modalCtrl.openModal().result;
                }

                function openIfClosed() {
                    if (scope.state = 'closed') {
                        return open();
                    } else {
                        console.warn('trying to open an opened modal', element)
                    }
                }

                element.on('click', function () {
                    openIfClosed().finally(function () {
                        scope.state = 'closed'
                    })
                }.bind(this));

            }
        }
    }
})();
