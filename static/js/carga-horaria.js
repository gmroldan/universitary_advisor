( function() {
	var app = angular.module('cargaHoraria', []);

	app.controller( 'CargaHorariaController', [ '$http', function($http) {
		this.dias = dias_const;
		this.disponibilidades = [
			{ dia_key: '1', modulos: [ '08:00:00', '08:45:00', '09:30:00' ] },
			{ dia_key: '2', modulos: [ '08:00:00', '08:45:00', '09:30:00' ] },
			{ dia_key: '3', modulos: [  ] },
			{ dia_key: '4', modulos: [ '10:15:00', '11:00:00', '11:45:00' ] },
			{ dia_key: '5', modulos: [ '10:15:00', '11:00:00', '11:45:00' ] },
		];


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
