
(function () {
    'use strict';
    //window.prefix = 'api/';
//this service handle all of the network connection

    angular.module('BlurAdmin.connection', [])
    //factory for the server connection
        .factory('ServerConnection', ['$http', '$rootScope', '$q','$localStorage',  function ($http, $rootScope, $q,$localStorage) {
            var connection =
                {
                    isLoading: false,
                    serverUrl: 'http://127.0.0.1:4000',//TODO add port

                    dataToUrl: function (data) {
                        let andUri = "?";
                        for (let key in data) {
                            andUri = andUri + key + "=" + data[key] + "&"
                        }
                        return andUri.substring(0, andUri.length - 1);
                    },

                    showLoading: function () {
                        this.isLoading = true
                    },

                    hideLoading: function () {
                        this.isLoading = false
                    },
                    sendGet: function (route, data = {}, cache, successFunc, errorFunc) {
                        this.showLoading();
                        var uri = this.dataToUrl(data);
                        return this.sendHttp('GET', null, this.serverUrl + route + uri, cache, successFunc, errorFunc);
                    },
                    sendPost: function (route, data = {}, routedata, cache, successFunc, errorFunc) {
                        this.showLoading();
                        if (routedata) {
                            var uri = this.dataToUrl([routedata]);
                            return this.sendHttp('POST', {}, this.serverUrl + route + uri, cache, successFunc, errorFunc);
                        }
                        else return this.sendHttp('POST', {...data, username:$localStorage.User.username,password:$localStorage.User.password}, this.serverUrl + route, cache, successFunc, errorFunc);
                    },
                    sendDelete: function (route, data = {}, cache, successFunc, errorFunc) {
                        return this.sendHttp('DELETE', data, this.serverUrl + route, cache, successFunc, errorFunc);
                    },
                    sendPut: function (route, data = {}, cache, successFunc, errorFunc) {
                        this.showLoading();
                        return this.sendHttp('PUT', data, this.serverUrl + route, cache, successFunc, errorFunc);
                    },

                    //sends an http request with the requested parameters
                    sendHttp: function (method, data, url, cache, successFunc, errorFunc, upload) {
                        var self = this;
                        var deferred = $q.defer();
                        var successFunction = function (response) {
                            self.hideLoading();
                            if (successFunc)
                                successFunc(response.data, deferred);
                            else {
                                deferred.resolve(response.data);
                            }
                        };

                        var errorFunction = function (response) {
                            self.hideLoading();
                            if (errorFunc)
                                errorFunc(response.data, deferred);
                            else {
                                $rootScope.$broadcast('error', {msg: response.data.message});
                                deferred.reject(response.data);
                            }
                        };

                        // if (localStorage.getItem("MA_user") && $rootScope.isIos)
                        //     header.cookie = JSON.parse(localStorage.getItem("MA_user")).sessionId;

                        $http({
                            method: method,
                            url: url,
                            data: JSON.stringify(data),
                            headers: {
                                'Access-Control-Allow-Credentials': true,
                               //  'Access-Control-Allow-Origin': true,

                            }
                        })
                            .then(successFunction,errorFunction)
                            //.error(errorFunction);
                        return deferred.promise;
                    },

                };

            return connection;
        }]).config(
        function ($httpProvider) {
            $httpProvider.defaults.useXDomain = true;
            $httpProvider.defaults.withCredentials = false; //TODO turn to true on release (CORS fix for dev)
            if (!$httpProvider.defaults.headers.get) {
                $httpProvider.defaults.headers.get = {};
            }
            // $httpProvider.defaults.headers.get['Cache-Control'] = 'no-cache';//TODO uncomment on release (CORS fix for dev)
            // $httpProvider.defaults.headers.get['Pragma'] = 'no-cache';//TODO uncomment on release (CORS fix for dev)
            delete $httpProvider.defaults.headers.common["X-Requested-With"];
        })
})();
