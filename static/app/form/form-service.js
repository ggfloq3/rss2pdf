(function () {
    angular.module('myApp').service('formService', function ($http) {
        delete $http.defaults.headers.common['X-Requested-With'];
        this.getData = function () {
            return $http({
                method: 'GET',
                url: '/data'
            });
        };
        this.sendData = function (data) {
            return $http({
                method: 'POST',
                url: '/',
                data: data,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (data) {

            });
        }
    });
})();