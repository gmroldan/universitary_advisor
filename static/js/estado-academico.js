( function() {
  var app = angular.module('estadoAcademico', []);

  app.controller( 'EstadoAcademicoController', [ '$http', function($http) {
      this.anios = anios_const;

      var est_acad = this;
      est_acad.materias = [];
      est_acad.regulares = [];
	  est_acad.aprobadas = [];


	  /**
	  * Methods to consume JSONs.
	  */
      $http.get('/universitary_advisor/estado_academico/getMaterias.json').success(function(data) {
          est_acad.materias = data.materias;
      });

      $http.get('/universitary_advisor/estado_academico/getRegulares.json').success(function(data) {
          est_acad.regulares = data.regulares;
      });

	  $http.get('/universitary_advisor/estado_academico/getAprobadas.json').success(function(data) {
          est_acad.aprobadas = data.aprobadas;
      });


	  /**
	  * Another methods.
	  */
      this.getCheckboxRegularesCSSClass = function(materia_id) {
          for (var i = 0; i < this.regulares.length; i++) {
              if (this.regulares[i] == materia_id) {
                  return css_class_active_checkbox_const;
              }
          }
          return css_class_inactive_checkbox_const;
      };


	  this.getCheckboxAprobadasCSSClass = function(materia_id) {
          for (var i = 0; i < this.aprobadas.length; i++) {
              if (this.aprobadas[i] == materia_id) {
                  return css_class_active_checkbox_const;
              }
          }
          return css_class_inactive_checkbox_const;
      };
  }]);

  var anios_const = [
    { key: '1', reference: 'collapseOne', description: '1º Año'},
    { key: '2', reference: 'collapseTwo', description: '2º Año' },
    { key: '3', reference: 'collapseThree', description: '3º Año' },
    { key: '4', reference: 'collapseFour', description: '4º Año' },
    { key: '5', reference: 'collapseFive', description: '5º Año' },
  ];

  var css_class_inactive_checkbox_const = 'btn btn-default';
  var css_class_active_checkbox_const = 'btn btn-default active';

} ) ();
