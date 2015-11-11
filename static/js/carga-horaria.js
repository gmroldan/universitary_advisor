( function() {
	var app = angular.module('cargaHoraria', []);

	app.controller( 'CargaHorariaController', [ '$http', function($http) {
		this.dias = dias_const;

		var carga_horaria = this;
		carga_horaria.horarios = [];

		/**
		* Methods to consume JSONs.
		*/
		$http.get('/universitary_advisor/modulo/carga_horaria.json').success(function(data) {
		  carga_horaria.horarios = data.horarios;
		});
	}]);

	var dias_const = [
		{ key: '1', description: 'Lunes'},
		{ key: '2', description: 'Martes' },
		{ key: '3', description: 'Miercoles' },
		{ key: '4', description: 'Jueves' },
		{ key: '5', description: 'Viernes' },
	];

} ) ();
