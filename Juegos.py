import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ORIGINS | FPS Zombies",
    page_icon="🧟",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background:#090a08;
    color:#d8bd83;
}
header,footer {
    visibility:hidden;
}
.block-container {
    padding:.5rem .7rem;
    max-width:100%;
}
h1 {
    color:#c99b49!important;
}
</style>
""", unsafe_allow_html=True)

st.title("☠ CALL OF DUTY: ZOMBIES — ORIGINS")
st.caption("FPS 3D · Supervivencia · Escenario original inspirado en Origins")

html = r"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

<style>
* {
    box-sizing:border-box;
}

html,body {
    margin:0;
    width:100%;
    height:100%;
    overflow:hidden;
    background:#090a08;
    font-family:Arial;
}

#stage {
    position:relative;
    width:100%;
    height:740px;
    overflow:hidden;
    background:#171710;
}

#stage.playing,
#stage.playing canvas {
    cursor:none!important;
}

canvas {
    display:block;
    width:100%;
    height:100%;
    outline:none;
}

#hud {
    position:absolute;
    z-index:4;
    top:12px;
    left:1%;
    width:98%;
    display:flex;
    justify-content:space-between;
    gap:6px;
    flex-wrap:wrap;
    pointer-events:none;
}

.stat {
    padding:8px 12px;
    color:#f0d49a;
    font-weight:bold;
    font-size:13px;
    letter-spacing:1px;
    background:rgba(5,6,5,.86);
    border:1px solid #a27b3d;
    text-shadow:0 1px 3px #000;
    backdrop-filter:blur(5px);
}

/* Retrato y vida del personaje */

#playerCard {
    position:absolute;
    z-index:6;
    left:14px;
    bottom:42px;
    width:210px;
    display:flex;
    align-items:center;
    gap:10px;
    padding:8px;
    background:rgba(5,6,5,.88);
    border:1px solid #a27b3d;
    color:#f0d49a;
    text-shadow:0 1px 3px #000;
    pointer-events:none;
}

#playerPortrait {
    width:58px;
    height:64px;
    flex:0 0 58px;
    border:1px solid #8f754b;
    background:linear-gradient(#555044,#171713);
    overflow:hidden;
}

#playerVitals {
    flex:1;
    font-size:12px;
    font-weight:bold;
    letter-spacing:1px;
}

#playerHealthTrack {
    height:10px;
    margin-top:7px;
    background:#271b16;
    border:1px solid #80613c;
}

#playerHealthFill {
    height:100%;
    width:100%;
    background:linear-gradient(90deg,#477b36,#a7bd55);
    transition:width .18s;
}

#playerSub {
    font-size:10px;
    color:#b8a783;
    margin-top:5px;
}

/* Mira */

#crosshair {
    position:absolute;
    z-index:5;
    left:50%;
    top:50%;
    width:22px;
    height:22px;
    transform:translate(-50%,-50%);
    pointer-events:none;
    border:1px solid rgba(255,242,207,.75);
    border-radius:50%;
    box-shadow:0 0 4px #000;
}

#crosshair:before,
#crosshair:after {
    content:"";
    position:absolute;
    background:#fff2cf;
    box-shadow:0 0 4px #000;
}

#crosshair:before {
    width:2px;
    height:8px;
    left:9px;
    top:-5px;
    box-shadow:0 24px 4px -1px #fff2cf;
}

#crosshair:after {
    height:2px;
    width:8px;
    top:9px;
    left:-5px;
    box-shadow:24px 0 4px -1px #fff2cf;
}

#crosshair.aiming {
    width:30px;
    height:30px;
    border:2px solid #f1d7a0;
}

#crosshair.aiming:before {
    height:5px;
    left:12px;
    top:-7px;
    box-shadow:0 35px 4px -1px #fff2cf;
}

#crosshair.aiming:after {
    width:5px;
    top:12px;
    left:-7px;
    box-shadow:35px 0 4px -1px #fff2cf;
}

#hitflash {
    position:absolute;
    inset:0;
    z-index:3;
    background:transparent;
    pointer-events:none;
}

#bottom {
    position:absolute;
    z-index:4;
    bottom:10px;
    left:0;
    width:100%;
    text-align:center;
    color:#e0d0ad;
    font-size:12px;
    text-shadow:0 2px 4px #000;
    pointer-events:none;
}

/* Menú */

#overlay {
    position:absolute;
    inset:0;
    z-index:10;
    display:flex;
    align-items:center;
    justify-content:center;
    background:rgba(0,0,0,.84);
    text-align:center;
}

#menu {
    width:min(92%,550px);
    padding:28px;
    color:#e5d1a4;
    background:rgba(15,15,12,.97);
    border:1px solid #b58b45;
    box-shadow:0 0 35px #000;
}

#menu h1 {
    margin:0 0 8px;
    color:#d0a04d;
    letter-spacing:4px;
}

#menu h2 {
    font-size:14px;
    letter-spacing:3px;
}

#start {
    margin:12px;
    padding:13px 28px;
    cursor:pointer;
    color:white;
    font-weight:bold;
    background:#76271d;
    border:1px solid #d0a04d;
}

#instructions {
    font-size:13px;
    color:#c9b991;
    line-height:1.8;
}

#status {
    min-height:22px;
}

#notice {
    font-size:11px;
    color:#bba77b;
    margin-top:10px;
}

/* Pantalla completa */

#fullBtn {
    position:absolute;
    z-index:8;
    right:12px;
    bottom:42px;
    padding:9px 12px;
    background:rgba(5,6,5,.88);
    border:1px solid #a27b3d;
    color:#f0d49a;
    font-weight:bold;
    cursor:pointer;
}

/* Caja misteriosa */

#boxPrompt {
    position:absolute;
    z-index:6;
    left:50%;
    bottom:72px;
    transform:translateX(-50%);
    display:none;
    padding:10px 16px;
    background:rgba(8,8,6,.9);
    border:1px solid #d2a44e;
    color:#f6d58c;
    font-weight:bold;
    text-align:center;
    pointer-events:none;
}

#boxPanel {
    position:absolute;
    z-index:12;
    inset:0;
    display:none;
    align-items:center;
    justify-content:center;
    background:rgba(0,0,0,.78);
}

#boxCard {
    width:min(92%,440px);
    padding:24px;
    background:linear-gradient(145deg,#27251d,#090a08);
    border:2px solid #bd9148;
    color:#f0d49a;
    text-align:center;
    box-shadow:0 0 35px #000;
}

#boxCard h2 {
    letter-spacing:3px;
    color:#d9aa54;
}

#boxCard button {
    margin:8px;
    padding:12px 20px;
    background:#70251c;
    color:white;
    border:1px solid #d6aa5b;
    font-weight:bold;
    cursor:pointer;
}

#boxResult {
    min-height:38px;
    color:#e6d6ae;
}

#pointsPop {
    position:absolute;
    z-index:7;
    left:50%;
    top:43%;
    transform:translateX(-50%);
    color:#f5d47b;
    font-size:20px;
    font-weight:bold;
    text-shadow:0 2px 5px #000;
    pointer-events:none;
    opacity:0;
    transition:opacity .15s;
}
</style>
</head>

<body>

<div id="stage">

    <div id="hud">
        <div class="stat">
            RONDA <span id="round">1</span>
        </div>

        <div class="stat">
            PUNTOS <span id="score">0</span>
        </div>

        <div class="stat">
            MUNICIÓN <span id="ammo">12 / 12</span>
        </div>

        <div class="stat">
            ZOMBIES RESTANTES <span id="count">0 / 9</span>
        </div>
    </div>

    <!-- Retrato del personaje y vida -->

    <div id="playerCard">

        <div id="playerPortrait" aria-label="Retrato del soldado">

            <svg viewBox="0 0 80 90" width="58" height="64"
                 xmlns="http://www.w3.org/2000/svg">

                <defs>
                    <linearGradient id="uniform" x2="0" y2="1">
                        <stop stop-color="#77745c"/>
                        <stop offset="1" stop-color="#292d26"/>
                    </linearGradient>
                </defs>

                <rect width="80" height="90" fill="#34352e"/>

                <path d="M8 90 Q10 61 28 55 L52 55 Q72 63 74 90"
                      fill="url(#uniform)"/>

                <path d="M24 32 Q20 9 40 8 Q61 10 56 35 L53 52 Q40 65 27 51Z"
                      fill="#b28e69"/>

                <path d="M20 29 Q18 4 41 4 Q63 5 61 29 L55 25 25 25Z"
                      fill="#3e4639"/>

                <path d="M23 24 L58 24 L55 32 L25 32Z"
                      fill="#252a24"/>

                <path d="M29 36 L36 36 M45 36 L52 36"
                      stroke="#211f1a"
                      stroke-width="3"
                      stroke-linecap="round"/>

                <path d="M34 48 Q40 52 47 47"
                      fill="none"
                      stroke="#573d31"
                      stroke-width="2"/>

                <path d="M29 57 L40 69 L51 57"
                      fill="none"
                      stroke="#a18a60"
                      stroke-width="4"/>

                <path d="M8 90 L15 69 L28 61 L40 72 L53 61 L67 70 L74 90"
                      fill="url(#uniform)"/>

                <path d="M6 90 L20 72 L30 80 L40 72 L51 80 L62 72 L76 90"
                      fill="#252a23"/>

            </svg>

        </div>

        <div id="playerVitals">
            <div>
                SOLDADO · VIDA <span id="health">100</span>
            </div>

            <div id="playerHealthTrack">
                <div id="playerHealthFill"></div>
            </div>

            <div id="playerSub">
                SUPERVIVENCIA ORIGINS
            </div>
        </div>

    </div>

    <div id="crosshair">+</div>
    <div id="hitflash"></div>

    <div id="pointsPop">+10</div>

    <div id="boxPrompt">
        PULSA E PARA USAR LA CAJA MISTERIOSA · 950 PUNTOS
    </div>

    <button id="fullBtn" type="button">
        ⛶ PANTALLA COMPLETA
    </button>

    <div id="boxPanel">
        <div id="boxCard">

            <h2>CAJA MISTERIOSA</h2>

            <p>Una nueva arma por 950 puntos.</p>

            <div id="boxResult">
                ¿Qué arma te tocará?
            </div>

            <button id="buyBox">
                ABRIR CAJA · 950
            </button>

            <button id="closeBox">
                CERRAR
            </button>

        </div>
    </div>

    <div id="bottom">
        WASD: MOVER · RATÓN: MIRAR · CLIC DERECHO: APUNTAR ·
        CLIC IZQUIERDO: DISPARAR · ESPACIO: SALTAR ·
        CAPS LOCK: AGACHARSE · R: RECARGAR · SHIFT: CORRER ·
        E: CAJA · ESC: PAUSAR
    </div>

    <div id="overlay">

        <div id="menu">

            <h1>ORIGINS</h1>

            <h2>FIRST PERSON SURVIVAL</h2>

            <p id="status">
                Sobrevive entre las ruinas. Consigue puntos y compra armas.
            </p>

            <button id="start">
                INICIAR PARTIDA
            </button>

            <div id="instructions">
                W A S D — moverse<br>
                Ratón — mirar alrededor<br>
                Clic derecho — apuntar<br>
                Clic izquierdo — disparar<br>
                ESPACIO — saltar · CAPS LOCK — agacharse<br>
                R — recargar · SHIFT — correr<br>
                E — usar la caja misteriosa
            </div>

            <div id="notice">
                Prototipo 3D original. Three.js se carga desde Internet.
            </div>

        </div>

    </div>

</div>

<script type="module">

import * as THREE from
"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";

const stage = document.getElementById("stage");

const scene = new THREE.Scene();

scene.background = new THREE.Color(0x625b4d);
scene.fog = new THREE.FogExp2(0x625b4d,.014);

const camera = new THREE.PerspectiveCamera(
    76,
    stage.clientWidth/stage.clientHeight,
    .1,
    220
);

camera.rotation.order = "YXZ";
camera.position.set(0,1.7,10);

const renderer = new THREE.WebGLRenderer({
    antialias:true
});

renderer.setPixelRatio(
    Math.min(devicePixelRatio || 1,1.6)
);

renderer.setSize(
    stage.clientWidth,
    stage.clientHeight
);

renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.shadowMap.autoUpdate = true;

renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.18;

stage.insertBefore(
    renderer.domElement,
    document.getElementById("hud")
);

renderer.domElement.tabIndex = 0;

/* Iluminación */

scene.add(
    new THREE.HemisphereLight(
        0xc6c0a7,
        0x30271c,
        1.35
    )
);

const sun = new THREE.DirectionalLight(
    0xffd6a0,
    2.0
);

sun.position.set(-18,30,14);
sun.castShadow = true;

sun.shadow.mapSize.set(4096,4096);
sun.shadow.bias = -0.00018;
sun.shadow.normalBias = 0.035;

sun.shadow.camera.left = -38;
sun.shadow.camera.right = 38;
sun.shadow.camera.top = 38;
sun.shadow.camera.bottom = -38;

scene.add(sun);

const warmFill = new THREE.DirectionalLight(
    0x8796a0,
    .42
);

warmFill.position.set(16,12,-18);
scene.add(warmFill);

const ambientGlow = new THREE.PointLight(
    0xd18b45,
    .65,
    34
);

ambientGlow.position.set(-8,3,-8);
scene.add(ambientGlow);

const boxGlow = new THREE.PointLight(
    0xffbd55,
    1.5,
    9
);

boxGlow.position.set(-4,2,-4);
scene.add(boxGlow);

/* Materiales */

function standard(color,rough=1,metal=0) {

    return new THREE.MeshStandardMaterial({
        color,
        roughness:rough,
        metalness:metal
    });

}

/* Texturas */

function noiseTexture(base,colors,count=15000) {

    const c = document.createElement("canvas");

    c.width = c.height = 512;

    const x = c.getContext("2d");

    x.fillStyle = base;
    x.fillRect(0,0,512,512);

    for(let i=0;i<count;i++) {

        x.globalAlpha = .2 + Math.random()*.65;

        x.fillStyle = colors[
            Math.floor(Math.random()*colors.length)
        ];

        const s = .5 + Math.random()*5;

        x.fillRect(
            Math.random()*512,
            Math.random()*512,
            s,
            s
        );

    }

    x.globalAlpha = 1;

    const t = new THREE.CanvasTexture(c);

    t.colorSpace = THREE.SRGBColorSpace;
    t.wrapS = t.wrapT = THREE.RepeatWrapping;

    return t;
}

const dirt = noiseTexture(
    "#62563f",
    [
        "#514633",
        "#77664a",
        "#403c31",
        "#88765a",
        "#59513f",
        "#6d6048"
    ]
);

dirt.repeat.set(18,18);

const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(180,180),
    new THREE.MeshStandardMaterial({
        map:dirt,
        roughness:1
    })
);

ground.rotation.x = -Math.PI/2;
ground.receiveShadow = true;

scene.add(ground);

const stoneTex = noiseTexture(
    "#70664f",
    [
        "#4f493b",
        "#92836a",
        "#5c5545",
        "#a09176"
    ],
    9000
);

stoneTex.repeat.set(2,2);

const stoneMat = new THREE.MeshStandardMaterial({
    map:stoneTex,
    roughness:1
});

/* Escenario */

const obstacles = [];

function wall(x,z,w,h,d,rot=0,color=0x75694f) {

    const m = new THREE.Mesh(
        new THREE.BoxGeometry(w,h,d),
        stoneMat
    );

    m.position.set(x,h/2,z);
    m.rotation.y = rot;

    m.castShadow = true;
    m.receiveShadow = true;

    scene.add(m);

    const ex =
        Math.abs(Math.cos(rot))*w/2 +
        Math.abs(Math.sin(rot))*d/2;

    const ez =
        Math.abs(Math.sin(rot))*w/2 +
        Math.abs(Math.cos(rot))*d/2;

    obstacles.push({
        minX:x-ex,
        maxX:x+ex,
        minZ:z-ez,
        maxZ:z+ez
    });

    return m;
}

function ruin(x,z,w,h,d) {

    wall(x,z,w,h,d,0);

    for(
        let i=0;
        i<Math.max(2,Math.floor(w/2));
        i++
    ) {

        const bw =
            w/Math.max(2,Math.floor(w/2))*.85;

        const px =
            x-w/2+
            (i+.5)*w/Math.max(2,Math.floor(w/2));

        const top = new THREE.Mesh(
            new THREE.BoxGeometry(bw,.35,d*.9),
            stoneMat
        );

        top.position.set(
            px,
            h+.12+(Math.random()-.5)*.3,
            z+(Math.random()-.5)*.15
        );

        top.rotation.y = (Math.random()-.5)*.08;

        top.castShadow = true;

        scene.add(top);
    }
}

ruin(-14,-13,10,7,6);
ruin(14,-16,11,9,6);
ruin(-16,14,10,8,7);
ruin(16,13,11,7,7);

wall(-25,0,5,10,50);
wall(25,0,5,10,50);
wall(0,-29,50,10,5);
wall(0,29,50,10,5);

wall(-10,-3,1.1,4,12);
wall(10,3,1.1,4,12);
wall(0,-17,14,5,1.2);
wall(-18,7,8,4,1.1);
wall(18,-7,8,4,1.1);

/* Sacos de arena */

const sackMat = standard(0x776747,1);

function sandbag(x,y,z,rot=0) {

    const bag = new THREE.Mesh(
        new THREE.SphereGeometry(.48,12,8),
        sackMat
    );

    bag.scale.set(1.25,.55,.72);
    bag.position.set(x,y,z);
    bag.rotation.y = rot;

    bag.castShadow = true;
    bag.receiveShadow = true;

    scene.add(bag);
}

for(let row=0;row<2;row++) {

    for(let i=0;i<7;i++) {

        sandbag(
            -7+i*1.05,
            .32+row*.48,
            -5+(row%2)*.35
        );

        sandbag(
            8+i*1.05,
            .32+row*.48,
            6+(row%2)*.35
        );

    }
}

/* Trincheras */

const trenchMat = standard(0x393326);

for(const side of [-1,1]) {

    const berm = new THREE.Mesh(
        new THREE.BoxGeometry(7,.55,1.1),
        trenchMat
    );

    berm.position.set(side*8,.12,13);
    berm.castShadow = true;
    berm.receiveShadow = true;

    scene.add(berm);
}

/* Faroles */

for(const [lx,lz] of [
    [-20,-5],
    [20,5],
    [-19,20],
    [19,-20]
]) {

    const pole = new THREE.Mesh(
        new THREE.CylinderGeometry(.09,.13,5,8),
        standard(0x393a34,.7,.5)
    );

    pole.position.set(lx,2.5,lz);
    pole.castShadow = true;

    scene.add(pole);

    const lamp = new THREE.Mesh(
        new THREE.BoxGeometry(.55,.22,.4),
        standard(0x282a25,.5,.4)
    );

    lamp.position.set(lx,4.95,lz);

    scene.add(lamp);
}

/* Cajas del escenario */

for(let i=0;i<10;i++) {

    const crate = new THREE.Mesh(
        new THREE.BoxGeometry(1.1,.8,.9),
        standard(0x494331)
    );

    crate.position.set(
        (Math.random()-.5)*34,
        .4,
        (Math.random()-.5)*34
    );

    crate.rotation.y = Math.random()*Math.PI;

    crate.castShadow = true;
    crate.receiveShadow = true;

    scene.add(crate);
}

/* Caja misteriosa */

const mysteryBox = new THREE.Group();

const boxBase = new THREE.Mesh(
    new THREE.BoxGeometry(1.35,.9,.85),
    standard(0x342d20,.65,.55)
);

boxBase.position.y = .48;
boxBase.castShadow = true;
boxBase.receiveShadow = true;

mysteryBox.add(boxBase);

const boxLid = new THREE.Mesh(
    new THREE.BoxGeometry(1.42,.16,.92),
    standard(0x5b482b,.45,.55)
);

boxLid.position.y = 1.02;
boxLid.castShadow = true;

mysteryBox.add(boxLid);

for(const side of [-1,1]) {

    const stripe = new THREE.Mesh(
        new THREE.BoxGeometry(.08,.75,.88),
        standard(0xb18436,.35,.6)
    );

    stripe.position.set(side*.48,.52,0);

    mysteryBox.add(stripe);
}

const boxLamp = new THREE.PointLight(
    0xffc45e,
    1.8,
    5
);

boxLamp.position.set(0,1.45,0);

mysteryBox.add(boxLamp);

mysteryBox.position.set(-4,0,-4);

scene.add(mysteryBox);

/* Muros del fondo */

for(let i=0;i<12;i++) {

    const x = -18+i*3.2;
    const h = 2.5+Math.random()*3.5;

    wall(x,-22,1.1,h,1.1);
}

/* Rocas */

for(let i=0;i<100;i++) {

    const rock = new THREE.Mesh(
        new THREE.DodecahedronGeometry(
            .2+Math.random()*.55
        ),
        standard(0x625943)
    );

    rock.position.set(
        (Math.random()-.5)*58,
        .15,
        (Math.random()-.5)*58
    );

    rock.rotation.set(
        Math.random()*3,
        Math.random()*3,
        Math.random()*3
    );

    rock.castShadow = true;

    scene.add(rock);
}

/* Árboles secos */

for(let i=0;i<10;i++) {

    const x = (Math.random()-.5)*55;
    const z = (Math.random()-.5)*55;

    if(Math.abs(x)<10 && Math.abs(z)<10) {
        continue;
    }

    const trunk = new THREE.Mesh(
        new THREE.CylinderGeometry(.12,.24,4,7),
        standard(0x30271d)
    );

    trunk.position.set(x,2,z);
    trunk.rotation.z = (Math.random()-.5)*.3;
    trunk.castShadow = true;

    scene.add(trunk);

    for(let j=0;j<3;j++) {

        const b = new THREE.Mesh(
            new THREE.CylinderGeometry(.04,.08,2,6),
            standard(0x30271d)
        );

        b.position.set(
            x+(Math.random()-.5),
            3+j*.2,
            z
        );

        b.rotation.z = (Math.random()-.5)*1.5;

        scene.add(b);
    }
}

/* Polvo ambiental */

const dustGeo = new THREE.BufferGeometry();
const dustPos = new Float32Array(360*3);

for(let i=0;i<360;i++) {

    dustPos[i*3] = (Math.random()-.5)*60;
    dustPos[i*3+1] = Math.random()*8;
    dustPos[i*3+2] = (Math.random()-.5)*60;

}

dustGeo.setAttribute(
    "position",
    new THREE.BufferAttribute(dustPos,3)
);

const dust = new THREE.Points(
    dustGeo,
    new THREE.PointsMaterial({
        color:0xd5c49b,
        size:.065,
        transparent:true,
        opacity:.4
    })
);

scene.add(dust);

/* Arma en primera persona */

const weapon = new THREE.Group();

const gunBody = new THREE.Mesh(
    new THREE.BoxGeometry(.22,.2,.72),
    standard(0x30352d,.55,.25)
);

gunBody.position.set(0,0,-.22);

weapon.add(gunBody);

const barrel = new THREE.Mesh(
    new THREE.CylinderGeometry(.043,.05,.58,12),
    standard(0x858477,.4,.7)
);

barrel.rotation.x = Math.PI/2;
barrel.position.set(0,.015,-.67);

weapon.add(barrel);

const grip = new THREE.Mesh(
    new THREE.BoxGeometry(.13,.3,.17),
    standard(0x554536)
);

grip.position.set(0,-.22,-.04);

weapon.add(grip);

const sight = new THREE.Mesh(
    new THREE.BoxGeometry(.08,.08,.16),
    standard(0xaaa18a,.4,.5)
);

sight.position.set(0,.13,-.35);

weapon.add(sight);

const sleeve = new THREE.Mesh(
    new THREE.BoxGeometry(.24,.25,.48),
    standard(0x494638)
);

sleeve.position.set(-.08,-.18,.12);

weapon.add(sleeve);

const glove = new THREE.Mesh(
    new THREE.BoxGeometry(.19,.13,.22),
    standard(0x292b25)
);

glove.position.set(-.06,-.12,-.12);

weapon.add(glove);

weapon.position.set(.36,-.31,-.72);

camera.add(weapon);
scene.add(camera);

const flash = new THREE.PointLight(
    0xffbd65,
    0,
    4
);

flash.position.set(0,0,-1);

camera.add(flash);

/* Estado de la partida */

const game = {
    health:100,
    score:0,
    ammo:12,
    maxAmmo:12,
    damage:1,
    weaponName:"PISTOLA M1911",
    round:1,
    speed:5,
    started:false,
    paused:false,
    over:false,
    reloading:false,
    damageCD:0,
    aiming:false,
    crouched:false,
    verticalVelocity:0,
    onGround:true,
    boxOpen:false
};

let zombies = [];
let keys = {};

let spawnTotal = 0;
let spawned = 0;
let spawnClock = 0;

let lastShot = 0;
let recoil = 0;

let mouseX = null;
let mouseY = null;

const standingHeight = 1.7;
const crouchHeight = 1.05;

const gravity = 19;
const jumpPower = 7.2;

const clock = new THREE.Clock();
const raycaster = new THREE.Raycaster();

/* Colisiones */

function collides(x,z,r=.42) {

    for(const o of obstacles) {

        const cx = Math.max(
            o.minX,
            Math.min(x,o.maxX)
        );

        const cz = Math.max(
            o.minZ,
            Math.min(z,o.maxZ)
        );

        if(
            (x-cx)**2+(z-cz)**2 < r*r
        ) {
            return true;
        }

    }

    return false;
}

function movePlayer(dx,dz) {

    const nx = camera.position.x+dx;
    const nz = camera.position.z+dz;

    if(!collides(nx,camera.position.z)) {
        camera.position.x = nx;
    }

    if(!collides(camera.position.x,nz)) {
        camera.position.z = nz;
    }

}

/* Crear zombies */

function makeZombie() {

    const group = new THREE.Group();

    const skin = standard(0x68764f);
    const coat = standard(0x343b31);
    const pants = standard(0x292c26);

    const torso = new THREE.Mesh(
        new THREE.BoxGeometry(.62,.88,.36),
        coat
    );

    torso.position.y = 1.12;

    group.add(torso);

    const head = new THREE.Mesh(
        new THREE.SphereGeometry(.27,16,12),
        skin
    );

    head.position.y = 1.76;

    group.add(head);

    const jaw = new THREE.Mesh(
        new THREE.BoxGeometry(.22,.09,.18),
        standard(0x343329)
    );

    jaw.position.set(0,1.61,.19);

    group.add(jaw);

    const tornCloth = new THREE.Mesh(
        new THREE.BoxGeometry(.64,.22,.38),
        standard(0x554333)
    );

    tornCloth.position.set(0,.78,0);

    group.add(tornCloth);

    const arms = [];

    for(const side of [-1,1]) {

        const eye = new THREE.Mesh(
            new THREE.SphereGeometry(.035,8,8),
            new THREE.MeshBasicMaterial({
                color:0xffc85b
            })
        );

        eye.position.set(
            side*.095,
            1.79,
            .235
        );

        group.add(eye);

        const arm = new THREE.Mesh(
            new THREE.BoxGeometry(.19,.72,.2),
            skin
        );

        arm.position.set(
            side*.42,
            1.15,
            .04
        );

        arm.rotation.z = side*.16;

        group.add(arm);

        arms.push(arm);

        const leg = new THREE.Mesh(
            new THREE.BoxGeometry(.23,.68,.25),
            pants
        );

        leg.position.set(
            side*.17,
            .38,
            0
        );

        group.add(leg);
    }

    group.traverse(o => {

        if(o.isMesh) {
            o.castShadow = true;
            o.receiveShadow = true;
        }

    });

    let a = Math.random()*Math.PI*2;
    const dist = 22+Math.random()*10;

    let x = camera.position.x+Math.cos(a)*dist;
    let z = camera.position.z+Math.sin(a)*dist;

    for(
        let tries=0;
        tries<12 && collides(x,z,.7);
        tries++
    ) {

        a += .55;

        x = camera.position.x+Math.cos(a)*dist;
        z = camera.position.z+Math.sin(a)*dist;

    }

    group.position.set(x,0,z);

    scene.add(group);

    /*
       La vida aumenta en cada ronda:
       Ronda 1 = 1 punto de vida.
       Ronda 2 = 2 puntos de vida.
       Ronda 3 = 3 puntos de vida.
       Y así sucesivamente.
    */

    const zombieHealth = game.round;

    zombies.push({
        mesh:group,
        hp:zombieHealth,
        maxHp:zombieHealth,
        speed:Math.min(
            1.65,
            .82+game.round*.055
        ),
        cooldown:0,
        phase:Math.random()*6,
        arms:arms
    });

}

/* Sistema de rondas */

function beginRound() {

    /*
       Ronda 1: 9 zombies.
       Ronda 2: 12 zombies.
       Ronda 3: 15 zombies.
       Aumenta 3 zombies por ronda.
       Máximo: 36 zombies por ronda.
    */

    spawnTotal = Math.min(
        6+game.round*3,
        36
    );

    spawned = 0;
    spawnClock = 1.0;

    showPoints(
        "RONDA "+game.round+
        " · "+spawnTotal+" ZOMBIES"
    );

}

/* HUD */

function hud() {

    document.getElementById("round").textContent =
        game.round;

    document.getElementById("score").textContent =
        game.score;

    document.getElementById("health").textContent =
        Math.ceil(game.health);

    const healthFill =
        document.getElementById("playerHealthFill");

    healthFill.style.width =
        Math.max(0,game.health)+"%";

    healthFill.style.background =
        game.health>60
        ? "linear-gradient(90deg,#477b36,#a7bd55)"
        : game.health>30
        ? "linear-gradient(90deg,#a66a24,#e0b34d)"
        : "linear-gradient(90deg,#7d1717,#e04432)";

    document.getElementById("ammo").textContent =
        game.reloading
        ? "RECARGANDO"
        : `${game.weaponName} · ${game.ammo} / ${game.maxAmmo}`;

    document.getElementById("count").textContent =
        `${zombies.length+spawnTotal-spawned} / ${spawnTotal}`;

    document.getElementById("boxPrompt").style.display =
        (
            camera.position.distanceTo(
                new THREE.Vector3(-4,0,-4)
            )<3.2 &&
            game.started &&
            !game.paused
        )
        ? "block"
        : "none";

}

function menu(text,button) {

    document.getElementById("status").textContent = text;

    document.getElementById("start").textContent = button;

    document.getElementById("overlay").style.display = "flex";

}

function clearZombies() {

    zombies.forEach(z => {
        scene.remove(z.mesh);
    });

    zombies = [];

}

/* Iniciar partida */

function startGame() {

    if(game.over) {

        clearZombies();

        game.health = 100;
        game.score = 0;
        game.ammo = 12;
        game.maxAmmo = 12;
        game.damage = 1;
        game.weaponName = "PISTOLA M1911";
        game.round = 1;

        game.over = false;
        game.reloading = false;
        game.boxOpen = false;

        camera.position.set(0,1.7,10);
        camera.rotation.set(0,0,0);

        spawnTotal = 0;
        spawned = 0;

    }

    game.started = true;
    game.paused = false;
    game.boxOpen = false;

    stage.classList.add("playing");

    document.getElementById("boxPanel").style.display = "none";
    document.getElementById("overlay").style.display = "none";

    if(spawnTotal===0) {
        beginRound();
    }

    hud();

    try {
        renderer.domElement.requestPointerLock();
    } catch(err) {
        document.getElementById("status").textContent =
            "El navegador no permitió capturar el cursor. Haz clic dentro del juego.";
    }

}

document.getElementById("start").addEventListener(
    "click",
    startGame
);

/* Puntos */

function showPoints(label) {

    const el = document.getElementById("pointsPop");

    el.textContent = label;
    el.style.opacity = "1";

    clearTimeout(showPoints.timer);

    showPoints.timer = setTimeout(() => {
        el.style.opacity = "0";
    },650);

}

/* Caja misteriosa */

function openMysteryBox() {

    if(
        !game.started ||
        game.paused ||
        game.over ||
        game.boxOpen
    ) {
        return;
    }

    if(
        camera.position.distanceTo(
            new THREE.Vector3(-4,0,-4)
        )>3.2
    ) {
        return;
    }

    game.boxOpen = true;
    game.paused = true;

    stage.classList.remove("playing");

    document.getElementById("boxPanel").style.display = "flex";

    document.exitPointerLock?.();

}

function closeMysteryBox() {

    game.boxOpen = false;

    document.getElementById("boxPanel").style.display = "none";

    if(!game.over) {

        game.paused = false;

        stage.classList.add("playing");

        renderer.domElement.requestPointerLock?.();

    }

}

/* Armas */

const weapons = [

    {
        name:"MP40",
        damage:1.25,
        ammo:32,
        description:"Subfusil · cargador de 32"
    },

    {
        name:"THOMPSON",
        damage:1.35,
        ammo:30,
        description:"Subfusil automático · cargador de 30"
    },

    {
        name:"STG-44",
        damage:1.6,
        ammo:25,
        description:"Fusil de asalto · cargador de 25"
    },

    {
        name:"BROWNING",
        damage:1.8,
        ammo:20,
        description:"Arma pesada · cargador de 20"
    },

    {
        name:"RAY GUN",
        damage:2.5,
        ammo:12,
        description:"Arma especial · daño aumentado"
    }

];

document.getElementById("buyBox").addEventListener(
    "click",
    () => {

        if(game.score<950) {

            document.getElementById("boxResult").textContent =
                "No tienes suficientes puntos. Necesitas 950.";

            return;
        }

        game.score -= 950;

        const prize = weapons[
            Math.floor(Math.random()*weapons.length)
        ];

        game.weaponName = prize.name;
        game.damage = prize.damage;
        game.maxAmmo = prize.ammo;
        game.ammo = prize.ammo;

        document.getElementById("boxResult").textContent =
            "¡OBTUVISTE: "+prize.name+"! "+prize.description;

        hud();

    }
);

document.getElementById("closeBox").addEventListener(
    "click",
    closeMysteryBox
);

/* Pantalla completa */

document.getElementById("fullBtn").addEventListener(
    "click",
    async (e) => {

        e.stopPropagation();

        try {

            if(!document.fullscreenElement) {
                await stage.requestFullscreen();
            } else {
                await document.exitFullscreen();
            }

        } catch(e) {

            document.getElementById("status").textContent =
                "El navegador no permitió pantalla completa.";

        }

    }
);

/* Recargar */

function reload() {

    if(
        !game.started ||
        game.paused ||
        game.reloading ||
        game.ammo===game.maxAmmo
    ) {
        return;
    }

    game.reloading = true;

    hud();

    setTimeout(() => {

        if(game.over) {
            return;
        }

        game.ammo = game.maxAmmo;
        game.reloading = false;

        hud();

    },1450);

}

/* Disparar */

function shoot() {

    if(
        !game.started ||
        game.paused ||
        game.over ||
        game.reloading ||
        game.ammo<=0
    ) {
        return;
    }

    const now = performance.now();

    if(now-lastShot<240) {
        return;
    }

    lastShot = now;

    game.ammo--;

    recoil = game.aiming ? .045 : .12;

    flash.intensity = 6;

    setTimeout(() => {
        flash.intensity = 0;
    },55);

    raycaster.setFromCamera(
        new THREE.Vector2(0,0),
        camera
    );

    let target = null;
    let nearest = Infinity;

    for(const z of zombies) {

        const center = z.mesh.position.clone();

        center.y = 1.15;

        const hit = raycaster.ray.intersectSphere(
            new THREE.Sphere(center,.72),
            new THREE.Vector3()
        );

        if(hit) {

            const d = camera.position.distanceTo(hit);

            if(d<nearest) {
                nearest = d;
                target = z;
            }

        }

    }

    const rayEnd = raycaster.ray.origin.clone().add(
        raycaster.ray.direction.clone().multiplyScalar(
            target ? nearest : 42
        )
    );

    const tracerGeo = new THREE.BufferGeometry().setFromPoints([
        camera.position.clone(),
        rayEnd
    ]);

    const tracer = new THREE.Line(
        tracerGeo,
        new THREE.LineBasicMaterial({
            color:0xffd28a,
            transparent:true,
            opacity:.8
        })
    );

    scene.add(tracer);

    setTimeout(() => {

        scene.remove(tracer);

        tracer.geometry.dispose();
        tracer.material.dispose();

    },65);

    if(target) {

        target.hp -= game.damage;

        game.score += 10;

        showPoints("+10 IMPACTO");

        if(target.hp<=0) {

            scene.remove(target.mesh);

            zombies = zombies.filter(z => z!==target);

            game.score += 90;

            showPoints("+90 ELIMINACIÓN");

        }

    }

    hud();

}

/* Controles del ratón */

document.addEventListener("mousedown",e => {

    if(!game.started || game.paused || game.over) {
        return;
    }

    if(e.button===0) {
        shoot();
    }

    if(e.button===2) {

        game.aiming = true;

        document.getElementById("crosshair")
            .classList.add("aiming");

        e.preventDefault();

    }

});

document.addEventListener("mouseup",e => {

    if(e.button===2) {

        game.aiming = false;

        document.getElementById("crosshair")
            .classList.remove("aiming");

    }

});

/* Daño al jugador */

function damage() {

    if(game.damageCD>0) {
        return;
    }

    game.health -= 8;

    game.damageCD = .9;

    const f = document.getElementById("hitflash");

    f.style.background = "rgba(150,0,0,.3)";

    setTimeout(() => {
        f.style.background = "transparent";
    },140);

    if(game.health<=0) {

        game.health = 0;

        game.over = true;
        game.started = false;

        stage.classList.remove("playing");

        document.exitPointerLock?.();

        menu(
            "HAS SIDO DERROTADO · PUNTOS: "+game.score,
            "VOLVER A JUGAR"
        );

    }

    hud();

}

/* Movimiento de los zombies */

function updateZombies(dt) {

    for(const z of zombies) {

        const dx = camera.position.x-z.mesh.position.x;
        const dz = camera.position.z-z.mesh.position.z;

        const dist = Math.hypot(dx,dz);

        z.phase += dt*7;

        if(z.arms.length===2) {

            z.arms[0].rotation.x =
                Math.sin(z.phase)*.42;

            z.arms[1].rotation.x =
                -Math.sin(z.phase)*.42;

        }

        if(dist>1.35) {

            const vx = dx/dist*z.speed*dt;
            const vz = dz/dist*z.speed*dt;

            const nx = z.mesh.position.x+vx;
            const nz = z.mesh.position.z+vz;

            if(!collides(nx,z.mesh.position.z,.38)) {
                z.mesh.position.x = nx;
            }

            if(!collides(z.mesh.position.x,nz,.38)) {
                z.mesh.position.z = nz;
            }

            z.mesh.rotation.y = Math.atan2(dx,dz);

            z.mesh.position.y =
                Math.abs(Math.sin(z.phase))*.04;

        } else {

            z.cooldown -= dt;

            if(z.cooldown<=0) {

                damage();

                z.cooldown = .85;

            }

        }

    }

}

/* Actualización de la partida */

function update(dt) {

    if(!game.started || game.paused || game.over) {
        return;
    }

    game.damageCD = Math.max(
        0,
        game.damageCD-dt
    );

    const f = new THREE.Vector3();

    camera.getWorldDirection(f);

    f.y = 0;
    f.normalize();

    /* Salto */

    if(keys[" "] && game.onGround) {

        game.verticalVelocity = jumpPower;
        game.onGround = false;

    }

    game.verticalVelocity -= gravity*dt;

    camera.position.y += game.verticalVelocity*dt;

    const desiredHeight =
        game.crouched
        ? crouchHeight
        : standingHeight;

    if(camera.position.y<=desiredHeight) {

        camera.position.y = desiredHeight;

        game.verticalVelocity = 0;

        game.onGround = true;

    }

    /* Movimiento del arma */

    const targetWeaponX =
        game.aiming ? .02 : .36;

    const targetWeaponY =
        game.aiming ? -.19 : -.31;

    weapon.position.x = THREE.MathUtils.lerp(
        weapon.position.x,
        targetWeaponX,
        Math.min(1,dt*12)
    );

    weapon.position.y = THREE.MathUtils.lerp(
        weapon.position.y,
        targetWeaponY,
        Math.min(1,dt*12)
    );

    /* Movimiento del jugador */

    const r = new THREE.Vector3(-f.z,0,f.x);
    const m = new THREE.Vector3();

    if(keys.w) m.add(f);
    if(keys.s) m.sub(f);
    if(keys.d) m.add(r);
    if(keys.a) m.sub(r);

    if(m.lengthSq()>0) {

        m.normalize();

        const speed =
            game.crouched
            ? 2.2
            : (keys.shift ? 7.2 : 5);

        movePlayer(
            m.x*speed*dt,
            m.z*speed*dt
        );

        if(
            game.onGround &&
            !game.crouched &&
            !game.aiming
        ) {

            const bob =
                Math.sin(performance.now()*.012)*.012;

            weapon.position.y = THREE.MathUtils.lerp(
                weapon.position.y,
                (game.aiming ? -.19 : -.31)+bob,
                Math.min(1,dt*8)
            );

        }

    }

    /* Límites del escenario */

    camera.position.x = THREE.MathUtils.clamp(
        camera.position.x,
        -23.8,
        23.8
    );

    camera.position.z = THREE.MathUtils.clamp(
        camera.position.z,
        -27.8,
        27.8
    );

    /* Sistema de aparición de zombies */

    spawnClock -= dt;

    /*
       El límite de zombies activos aumenta con las rondas.
       Nunca habrá más de 18 zombies activos al mismo tiempo.
    */

    const fieldLimit = Math.min(
        6+game.round,
        18
    );

    if(
        spawned<spawnTotal &&
        zombies.length<fieldLimit &&
        spawnClock<=0
    ) {

        makeZombie();

        spawned++;

        spawnClock = Math.max(
            .48,
            1.25-game.round*.025
        );

    }

    updateZombies(dt);

    /* Siguiente ronda */

    if(
        spawned>=spawnTotal &&
        zombies.length===0
    ) {

        game.round++;

        beginRound();

    }

    /* Retroceso del arma */

    recoil = Math.max(
        0,
        recoil-dt*.8
    );

    weapon.position.z = THREE.MathUtils.lerp(
        weapon.position.z,
        game.aiming ? -.55 : -.72,
        Math.min(1,dt*10)
    )+recoil;

    weapon.rotation.x = -recoil*.7;

    hud();

}

/* Animación del polvo */

function animateDust() {

    const p = dust.geometry.attributes.position;

    for(let i=0;i<p.count;i++) {

        p.array[i*3+1] += .001;

        if(p.array[i*3+1]>8) {
            p.array[i*3+1] = 0;
        }

    }

    p.needsUpdate = true;

}

/* Bucle de animación */

function animate() {

    requestAnimationFrame(animate);

    const dt = Math.min(
        clock.getDelta(),
        .05
    );

    update(dt);

    animateDust();

    mysteryBox.rotation.y =
        Math.sin(performance.now()*.0005)*.035;

    renderer.render(scene,camera);

}

animate();

/* Cámara: movimiento del ratón */

function rotateView(dx,dy) {

    camera.rotation.order = "YXZ";

    camera.rotation.y -= dx*.0022;
    camera.rotation.x -= dy*.0022;

    camera.rotation.x = THREE.MathUtils.clamp(
        camera.rotation.x,
        -1.42,
        1.42
    );

}

stage.addEventListener("mousemove",e => {

    if(!game.started || game.paused || game.over) {
        return;
    }

    if(
        document.pointerLockElement===
        renderer.domElement
    ) {

        rotateView(
            e.movementX,
            e.movementY
        );

        mouseX = null;
        mouseY = null;

        return;

    }

    /*
       Respaldo para touchpad cuando el navegador
       no permite capturar el cursor en el iframe.
    */

    const rect = stage.getBoundingClientRect();

    const x = e.clientX-rect.left;
    const y = e.clientY-rect.top;

    if(mouseX!==null && mouseY!==null) {

        const dx = x-mouseX;
        const dy = y-mouseY;

        if(
            Math.abs(dx)<120 &&
            Math.abs(dy)<120
        ) {

            rotateView(dx,dy);

        }

    }

    mouseX = x;
    mouseY = y;

});

stage.addEventListener("mouseenter",e => {

    mouseX = e.offsetX;
    mouseY = e.offsetY;

});

stage.addEventListener("mouseleave",() => {

    mouseX = null;
    mouseY = null;

});

stage.addEventListener("click",() => {

    if(
        game.started &&
        !game.paused &&
        !game.over &&
        document.pointerLockElement!==renderer.domElement
    ) {

        renderer.domElement.requestPointerLock?.();

    }

});

stage.addEventListener(
    "contextmenu",
    e => e.preventDefault()
);

/* Teclado */

window.addEventListener("keydown",e => {

    const k = e.key.toLowerCase();

    keys[k] = true;

    if([
        "w",
        "a",
        "s",
        "d",
        " ",
        "capslock"
    ].includes(k)) {

        e.preventDefault();

    }

    if(k==="capslock" && !e.repeat) {
        game.crouched = !game.crouched;
    }

    if(k==="r") {
        reload();
    }

    if(k==="e") {
        openMysteryBox();
    }

    if(
        k==="escape" &&
        game.started &&
        !game.over
    ) {

        game.paused = true;

        stage.classList.remove("playing");

        document.exitPointerLock?.();

        menu(
            "PARTIDA PAUSADA",
            "CONTINUAR"
        );

    }

});

window.addEventListener("keyup",e => {

    keys[e.key.toLowerCase()] = false;

});

window.addEventListener("blur",() => {

    game.aiming = false;

    document.getElementById("crosshair")
        .classList.remove("aiming");

});

/* Control de Pointer Lock */

document.addEventListener(
    "pointerlockchange",
    () => {

        if(
            game.started &&
            !game.over &&
            document.pointerLockElement!==renderer.domElement &&
            !game.paused
        ) {

            mouseX = null;
            mouseY = null;

        }

    }
);

/* Ajustar pantalla */

function resizeGame() {

    const w = stage.clientWidth;
    const h = stage.clientHeight;

    camera.aspect = w/h;

    camera.updateProjectionMatrix();

    renderer.setSize(w,h);

}

window.addEventListener(
    "resize",
    resizeGame
);

document.addEventListener(
    "fullscreenchange",
    () => {

        stage.style.height =
            document.fullscreenElement
            ? "100vh"
            : "740px";

        setTimeout(
            resizeGame,
            80
        );

    }
);

hud();

</script>
</body>
</html>
"""

components.html(
    html,
    height=750,
    scrolling=False
)

st.caption(
    "FPS 3D · Caja misteriosa · Puntos por impacto y eliminación · "
    "Rondas progresivas · Pantalla completa"
)