(function () {
    angular.module('myApp').controller('formController', function ($scope, formService) {
        $scope.date = $scope.date2 = {};
        $scope.userEmail = '';
        $scope.selectedCategories = [];
        $scope.dateOpts = {
            locale: {
                firstDay: 1
            },
            ranges: {
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()]
            }
        };

        formService.getData().then(function (dataResponse) {
            $scope.categoriesArr = dataResponse.data.categories;
            $scope.dateMin = dataResponse.data.date_min;
            $scope.dateMax = dataResponse.data.date_max;
        });

        $scope.onSubmit = function () {
            var form = $scope.multipleSelectForm;
            var ids = [];
            var data;

            if ($scope.multipleSelectForm.$invalid) {
                $scope.multipleSelectError = form.$error.required;
                $scope.emailError = form.input.$error.required || form.input.$error.email;
                $scope.dateError = form.daterange2.$error.required;
                return null;
            }

            $scope.selectedCategories.forEach(function (item, i, arr) {
                ids.push(item['id'])
            });

            data = {
                'email': $scope.userEmail,
                'categories': ids,
                'date1' :$scope.date.startDate.format('YYYY-MM-DD'),
                'date2' :$scope.date.endDate.format('YYYY-MM-DD')
            };
            formService.sendData(data).then(function (dataResponse) {
                if (dataResponse.data.success) {
                    $scope.hideForm = true;
                    $scope.message = dataResponse.data.message;
                } else {
                    $scope.message = dataResponse.data.errors;
                }
            });
        };
    });
})();