
window.pokeparty = {};
window.pokeparty.pokemon_list = [];
window.pokeparty.pokemon_svgs = {};

fetch("static/data/pokemon.json").then(resp => resp.json()).then((raw_data) => {
    for(id in raw_data) {
        let slug = raw_data[id].slug.eng;
        (async (slug) => {
            await fetch("static/img/pokesprite/pokemon-gen8/regular/"+slug+".svg")
                    .then(resp => {
                        if(resp.status == 200) {
                            return Promise.resolve(resp.text());
                        } 
                        return Promise.reject(resp.json());
                    })
                    .then(data => {
                        window.pokeparty.pokemon_svgs[slug] = data;
                        window.pokeparty.pokemon_list.push(slug);
                    })
                    .catch(error => console.error(error.message));
        })(slug);
    }
});

function createPokemonBubble() {
    const welcome = document.getElementById("welcome");
    const new_pokemon = document.createElement("object");
    new_pokemon.type = "image/svg+xml";
    var size = Math.random() * 40;

    if(window.pokeparty.pokemon_list.length == 0) {
        new_pokemon.data = "static/img/pokesprite/pokemon-gen8/regular/bulbasaur.svg";
    } else {
        new_pokemon.innerHTML = window.pokeparty.pokemon_svgs[window.pokeparty.pokemon_list[Math.floor(Math.random() * window.pokeparty.pokemon_list.length)]];
    }
    new_pokemon.className = "pokemon";
    new_pokemon.style.animation = "animation 6s linear infinite";
    new_pokemon.style.width = 54 + size + "px";
    new_pokemon.style.zIndex = 5;
    new_pokemon.style.left = Math.random() * innerWidth + "px";
    welcome.appendChild(new_pokemon);
    setTimeout(() => {
        new_pokemon.remove()
    }, 5000);
}

setInterval(createPokemonBubble, 250);