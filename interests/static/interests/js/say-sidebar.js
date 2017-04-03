(function(){
  //
  // Module and contollers for the main nav side bar
  //
  var app = angular.module('saySidebar', []);

  app.controller('SidebarController', function(){
    this.createOnly = false;
    this.activeTab = 0;
    this.toggleUser = false;
    this.toggleCreate = false;

    this.setActiveTab = function(tab){
      this.activeTab = tab;
    };

    this.isActive = function(tab){
      return this.activeTab === tab;
    };

  });
})();
