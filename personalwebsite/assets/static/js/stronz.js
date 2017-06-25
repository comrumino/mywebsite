var app = angular.module('personalwebsite', []);
app.controller('home', ['$scope', function($scope) {
  $scope.visible = false;
}]);
app.controller('portfolio', ['$scope', function($scope) {
  $scope.visible = false;
}]);
app.controller('about-me', ['$scope', function($scope) {
  $scope.visible = false;
}]);
