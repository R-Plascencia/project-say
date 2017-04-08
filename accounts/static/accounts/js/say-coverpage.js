(function(){
  //
  // Module and controllers for the Cover Page
  //
  var app = angular.module('sayCoverPage', ['ngAnimate']);

  app.controller('CoverController',['$scope', function($scope){
    this.activeLink = 1;  // Start with the 'Welcome' link set active
    $scope.user = {};
    this.regBtnClicked = false;
    this.loginBtnClicked = false;

    this.setActiveLink = function(link){
      this.activeLink = link;
    };

    this.isActiveLink = function(link){
      return this.activeLink === link;
    };

  }]);

})();
