(function(){
  //
  // Module and controllers for the Cover Page
  //
  var app = angular.module('sayCoverPage', []);

  app.controller('CoverController', function(){
    this.activeLink = 1;  // Start with the 'Welcome' link set active

    this.setActiveLink = function(link){
      this.activeLink = link;
    };

    this.isActiveLink = function(link){
      return this.activeLink === link;
    };
  });


})();
