CREATE TABLE main (
	time VARCHAR(20),
	temperature NUMERIC, 
	humidity NUMERIC, 
	noise NUMERIC, 
	isPeopleDetected BOOLEAN, 
	TVoC NUMERIC, 
	CO2eq NUMERIC,
	alerte_aeration BOOLEAN, 
	alerte_intrusion BOOLEAN, 
	alerte_incendie BOOLEAN, 
	visages NUMERIC
);

DROP TABLE main;


Select * from main;
