create table refugio(
	ID_refugio serial primary key,
	direccion  varchar(30),
	cantidad_perros integer default 0
);


create table voluntario(
	nombre varchar(20),
	apellido varchar(20),
	fecha_registro date,
	fecha_nacimiento date,
	telefono varchar(10),
	id_refugio integer,
	id_voluntario serial,
	PRIMARY KEY (id_voluntario),
	FOREIGN KEY (id_refugio) REFERENCES refugio(id_refugio)
);

CREATE TABLE perro(
	adoptado boolean,
	raza varchar (20),
	edad smallint,
	nombre varchar(10),
	fecha_ingreso date,
	id_refugio integer,
	id_perro serial,
	PRIMARY KEY (id_perro),
	FOREIGN KEY (id_refugio) REFERENCES refugio(id_refugio)
);


create table  patrocinador(
	nombre varchar(20),
	telefono varchar(10),
	id_patrocinador serial,
	PRIMARY KEY (id_patrocinador)
);

create table patrocinios(
	id_patrocinador integer,
	id_refugio integer,
	id_patrocinio serial primary key,
	FOREIGN KEY (id_patrocinador) REFERENCES patrocinador(id_patrocinador),
	FOREIGN KEY (id_refugio) REFERENCES refugio(id_refugio)
);

CREATE TABLE adoptante(
	telefono varchar(15),
	nombre varchar(30),
	domicilio varchar(30),
	id_adoptante serial primary key
);

CREATE TABLE adopcion(
	id_adopcion serial,
	fecha_adopcion date,
	id_refugio integer,
	id_perro integer,
	id_adoptante integer,
	PRIMARY KEY (id_adopcion),
	FOREIGN KEY (id_refugio) REFERENCES refugio(id_refugio),
	FOREIGN KEY (id_perro) REFERENCES perro(id_perro),
	FOREIGN KEY (id_adoptante) REFERENCES adoptante(id_adoptante)
);

create function update_perro_adoptado() returns trigger
as $$
begin
update perro set adoptado=true where(id_perro = new.id_perro);
return new;
end
$$
language plpgsql;


create trigger TR_update_perro_adoptado_estado
after insert on adopcion
for each row
execute procedure update_perro_adoptado();



create function update_refugio_cantidad_perros() returns trigger
as $$
begin
update refugio set cantidad_perros=(cantidad_perros+1) where(id_refugio = new.id_refugio);
return new;
end
$$
language plpgsql;



create trigger TR_update_refugio_cant_perros_ingreso after insert on perro
for each row
execute procedure update_refugio_cantidad_perros();



create function update_refugio_cantidadperros_adoptados() returns trigger
as $$
begin
update refugio set cantidad_perros=(cantidad_perros-1) where(id_refugio = new.id_refugio);
return new;
end
$$
language plpgsql;
create trigger TR_update_refugio_cantidad_perros_adoptados
after insert on adopcion
for each row
execute procedure update_refugio_cantidadperros_adoptados();