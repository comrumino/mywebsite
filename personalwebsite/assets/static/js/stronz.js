var app = angular.module('personalwebsite', []);
app.controller('home', ['$scope', function($scope) {
  $scope.visible = false;
}]);
app.controller('blog', ['$scope', function($scope) {
  $scope.visible = false;
}]);
app.controller('portfolio', ['$scope', function($scope) {
  $scope.visible = false;
}]);
app.controller('contact', ['$scope', function($scope) {
  $scope.visible = false;
}]);
