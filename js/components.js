function getPeriode(ref) {
    var periode = 0;
    for (i = 1 ; i < danse.length ; i++) {
          if(ref >= danse[i].debut) periode++;
    }
    return periode;
}

// CHARGEMENT MODELE
AFRAME.registerComponent('model_loaded', {
    init: function() {
        var el = this.el;
        el.addEventListener('model-loaded', () => {
            console.log(">>>> modele chargé "+el.id);
        });
        el.addEventListener('model-error', () => {
              console.log(">>>> modele erreur"+el.id);
            });
    }
});
// SHADOW MATERIAL : 1 parametre opacite
AFRAME.registerComponent('shadow-material', {
    schema: {
        opacite: {type: 'number', default: 0.5}
    },
    init: function(){
        let el = this.el;
        let mesh = el.getObject3D('mesh');
        // console.log(mesh);
        if (!mesh){return;}
        mesh.material = new THREE.ShadowMaterial();
        mesh.material.opacity = this.data.opacite;
    }
});

// DEMARRAGE ANIM = READY (delai après démarrage audio) :
// 2 parametres :
// - audio    = id de l'audio
// - delai    = attente en ms avant de lancer anim
// ----------------------------------------------------------
AFRAME.registerComponent('delay_ready', {
  schema: {
        audio: {type: 'string', default: ''},
        delai: {type: 'number', default: 1000},
  },
  init: function () {
      var el = this.el;
      var delai = this.data.delai;
      const son = document.getElementById(this.data.audio);
      son.addEventListener('playing', (event) => {
          playing = true;
          setTimeout(function() {
              var animdata = "clip: ready; crossFadeDuration: 0.3; repetitions: 1; duration: 1;"
              console.log(el.id+"_ animdata"+animdata);
              el.removeAttribute("animation-mixer");
              el.setAttribute("animation-mixer", animdata);
              pas_current = "ready";
              var pas = document.querySelector('#pas');
              pas.innerHTML = animdata;
          }, delai);
      });
  }
});

AFRAME.registerComponent('sirtaki', {
    init: function() {
        var el = this.el;
        el.addEventListener('animation-finished', () => {
            var clip = Math.floor((Math.random() * 5) + 1 );
            var repet = Math.floor((Math.random() * 3) + 1 );
            var animdata = "clip: pas_0"+clip+"; crossFadeDuration: 0.3; repetitions: 1; ";
            var speed = danse[periode].vitesse;
            animdata = animdata + "duration: "+(duree_pas[clip]/speed).toFixed(1)+";"
            console.log("animdata : "+animdata);
            el.removeAttribute("animation-mixer");
            el.setAttribute("animation-mixer", animdata);
            var pas = document.querySelector('#pas');
            pas.innerHTML = animdata;
        });
    }
});
