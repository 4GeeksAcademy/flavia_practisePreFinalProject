const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			demo: [
				{
					title: "FIRST",
					background: "white",
					initial: "white"
				},
				{
					title: "SECOND",
					background: "white",
					initial: "white"
				}
			],
			actors : [
				{
					nombre: "PRUEBA",
					nacionalidad:"PRUEBA"
				}
			],
			specificActor : null
		},
		actions: {
			// Use getActions to call a function within a fuction
			exampleFunction: () => {
				getActions().changeColor(0, "green");
			},

			getActors : () => {
				console.log("getActors from flux")
				fetch(process.env.BACKEND_URL +"/api/actors")
				.then((response) => response.json())
				.then((data) => {
					console.log("Dati ricevuti:", data);
					setStore({actors : data})
				})
				
			},

			getSpecificActor : (actorId) => { 
				console.log("getActors from flux")
				fetch(process.env.BACKEND_URL +"/api/actors/" + actorId)
				.then((response) => response.json())
				.then((data) => {
					console.log("Dati ricevuti:", data);
					setStore({specificActor : data})
				})	
			},

			addActor : (newActor) => {
				console.log("addActor from flux")

				const requestOptions = {
					method : "POST",
					headers: {"Content-Type" : "application/json"},
					body: JSON.stringify(newActor)
				} 

				fetch(process.env.BACKEND_URL +"/api/actors", requestOptions)
				.then((response) => response.json())
				.then((data) => {	
					const store = getStore();
					setStore({actors: [...store.actors, data]})
				});
			},

			deleteActor : (actorId) => {
				const requestOptions = {
					method : "DELETE",
					headers: {"Content-Type" : "application/json"},
				} 
				fetch(process.env.BACKEND_URL +"/api/actors/" + actorId, requestOptions)
				.then((response) => response.json())
				.then((data) => {
					console.log("Actor to delete:", data);
					const store = getStore();
					setStore({actors : store.actors.filter(actor => actor.id !== actorId)})
				})	
			},
			
			modifyActor : (actorId, updatedActor) => {
				const requestOptions = {
					method : "PUT",
					headers: {"Content-Type" : "application/json"},
					body: JSON.stringify(updatedActor)                               // Usa i dati aggiornati
				};

				fetch(process.env.BACKEND_URL +"/api/actors/" + actorId, requestOptions)
				.then((response) => response.json())            
				.then((data) => {
					console.log("Actor updated:", data);

					const store = getStore();
					// Aggiorna la lista sostituendo l'attore modificato:
					const updatedActors = store.actors.map(actor => 
						actor.id === actorId ? data : actor
					);
					setStore({ actors: updatedActors });
				})	
			},


			getMessage: async () => {
				try{
					// fetching data from the backend
					const resp = await fetch(process.env.BACKEND_URL + "/api/hello")
					const data = await resp.json()
					setStore({ message: data.message })
					// don't forget to return something, that is how the async resolves
					return data;
				}catch(error){
					console.log("Error loading message from backend", error)
				}
			},
			changeColor: (index, color) => {
				//get the store
				const store = getStore();

				//we have to loop the entire demo array to look for the respective index
				//and change its color
				const demo = store.demo.map((elm, i) => {
					if (i === index) elm.background = color;
					return elm;
				});

				//reset the global store
				setStore({ demo: demo });
			}
		}
	};
};

export default getState;
