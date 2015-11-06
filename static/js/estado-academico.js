( function() {
  var app = angular.module('estadoAcademico', []);

  app.controller( 'EstadoAcademicoController', [ '$http', function($http) {
      this.anios = anios_const;

      var est_acad = this;
      est_acad.materias = [];

	  /**
	  * Methods to consume JSONs.
	  */
      $http.get('/universitary_advisor/estado_academico/index.json').success(function(data) {
          est_acad.materias = data.materias_dto;
      });
  }]);

  var anios_const = [
    { key: '1', reference: 'collapseOne', description: '1º Año'},
    { key: '2', reference: 'collapseTwo', description: '2º Año' },
    { key: '3', reference: 'collapseThree', description: '3º Año' },
    { key: '4', reference: 'collapseFour', description: '4º Año' },
    { key: '5', reference: 'collapseFive', description: '5º Año' },
  ];

} ) ();
