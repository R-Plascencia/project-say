(function(){
  //
  // Module and contollers for the main nav side bar
  //
  var app = angular.module('saySidebar', []);

  app.controller('SidebarController',['$location', '$log', '$scope', function($location, $log, $scope){
    this.createOnly = false;
    this.toggleUser = false;
    this.toggleCreate = false;

    $scope.currentUrl = $location.path();
    $log.info($scope.currentUrl);
    this.activeTab = 1;
    if ($scope.currentUrl === '/interests/list/'){
      this.activeTab = 2;
    }
    if ($scope.currentUrl === '/about/'){
      this.activeTab = 3;
    }

    this.setActiveTab = function(tab){
      this.activeTab = tab;
    };

    this.isActive = function(tab){
      return this.activeTab === tab;
    };

  }]);

  app.controller('CreationController', function(){
    this.interest = {};
    this.btnClicked = false;
    this.createOnly = false;
  });
})();
