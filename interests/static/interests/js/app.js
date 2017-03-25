var app = angular.module('interestApp', []);

// // Avoid Django and NG template tag collision
// app.config(function($interpolateProvider){
//   $interpolateProvider.startSymbol('{$');
//   $interpolateProvider.endSymbol('$}');
// });

app.controller('CreationController', function(){
  this.interest = {};

});
