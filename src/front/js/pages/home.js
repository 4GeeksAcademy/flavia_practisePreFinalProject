import React, { useState, useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";

export const Home = () => {
	const { store, actions } = useContext(Context);

	useEffect(() => {
		actions.getActors();
	},[]) ;

	return (
		<div className="text-center mt-5">
			<h1>Lista actores</h1>
			<button type="button" className="btn btn-primary" onClick={() => actions.addActor({nombre: "Nuevo Actor", nacionalidad: "Desconocida"})}>Crea nuevo actor</button>
			<ul>
				{
					store.actors.map((actor) => {
						return (
						<li key={actor.id}>
							<span><strong>ID:</strong>{actor.id} </span><span><strong>Nombre:</strong> {actor.nombre} </span><span><strong>Nacionalidad:</strong> {actor.nacionalidad}</span>
							<div>
								<button onClick={() => actions.modifyActor(actor.id, { nombre: "Modificado", nacionalidad: "Actualizada" })}>modifica actor</button>
								<button onClick={() => actions.deleteActor(actor.id)}>elimina actor</button>
							</div>
						</li>
						)
					})
				}
			</ul>
		</div>
	);
};
