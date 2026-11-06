
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ORIGINS - Zombie Survival",
    page_icon="🧟",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #090a08;
    color: #e6d2a7;
}
header, footer {
    visibility: hidden;
}
.block-container {
    padding: .5rem;
    max-width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("☠ ORIGINS — ZOMBIE SURVIVAL")
st.caption("Supervivencia FPS · Escenario 3D · Control con touchpad")

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; }

html, body {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #111;
    font-family: Arial, sans-serif;
}

#stage {
    position: relative;
    width: 100%;
    height: 740px;
    overflow: hidden;
    background: #27251e;
    touch-action: pan-y;
}

canvas {
    display: block;
    width: 100%;
    height: 100%;
    outline: none;
}

#hud {
    position: absolute;
    z-index: 5;
    top: 12px;
    left: 1%;
    width: 98%;
    display: flex;
    justify-content: space-between;
    gap: 5px;
    flex-wrap: wrap;
    pointer-events: none;
}

.stat {
    background: rgba(5,5,4,.88);
    border: 1px solid #9d8049;
    color: #f0d9a5;
    padding: 9px 13px;
    font-size: 13px;
    font-weight: bold;
    text-shadow: 0 2px 3px black;
}

#cross {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%,-50%);
    color: white;
    font-size: 23px;
    text-shadow: 0 0 5px black;
    pointer-events: none;
}

#bottom {
    position: absolute;
    bottom: 10px;
    width: 100%;
    text-align: center;
    color: white;
    font-size: 12px;
    text-shadow: 0 2px 4px black;
    pointer-events: none;
}

#overlay {
    position: absolute;
    inset: 0;
    z-index: 10;
    background: rgba(0,0,0,.9);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

#menu {
    padding: 30px;
    width: min(92%, 520px);
    background: #11120f;
    border: 1px solid #b18a48;
    color: #e9d6ac;
}

#menu h1 {
    font-size: 38px;
    letter-spacing: 7px;
    color: #c59a4c;
}

#menu p {
    line-height: 1.7;
}

button {
    background: #782b1e;
    color: white;
    border: 1px solid #d3ad6c;
    padding: 13px 35px;
    font-weight: bold;
    cursor: pointer;
}

.small {
    font-size: 12px;
    color: #c6b58e;
    line-height: 1.9;
}
</style>
</head>

<body>
<div id="stage">

    <div id="hud">
        <div class="stat">RONDA: <span id="round">1</span></div>
        <div class="stat">PUNTOS: <span id="score">0</span></div>
        <div class="stat">VIDA: <span id="health">100</span></div>
        <div class="stat">MUNICIÓN: <span id="ammo">12 / 12</span></div>
        <div class="stat">ZOMBIES: <span id="count">0</span></div>
    </div>

    <div id="cross">+</div>

    <div id="bottom">
        WASD: MOVERSE · TOUCHPAD: DESLIZAR · CLIC IZQUIERDO: DISPARAR ·
        SHIFT: CORRER · R: RECARGAR · ESC: PAUSAR
    </div>

    <div id="overlay">
        <div id="menu">
            <h1>ORIGINS</h1>
            <p id="status">
                Sobrevive entre las ruinas. Los zombis se acercan.
            </p>

            <button id="start">INICIAR PARTIDA</button>

            <p class="small">
                W A S D — Movimiento<br>
                Deslizar touchpad sin presionar — Girar cámara<br>
                Clic izquierdo — Disparar<br>
                SHIFT — Correr<br>
                R — Recargar<br>
                ESC — Pausar
            </p>
        </div>
    </div>
</div>

<script type="module">
import * as THREE from
"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";

// ==================================================
// CONFIGURACIÓN GENERAL
// ==================================================

const stage = document.getElementById("stage");

const scene = new THREE.Scene();

scene.background = new THREE.Color(0x777365);
scene.fog = new THREE.FogExp2(0x777365, 0.010);

const camera = new THREE.PerspectiveCamera(
    76,
    stage.clientWidth / stage.clientHeight,
    0.1,
    250
);

camera.rotation.order = "YXZ";
camera.position.set(0, 1.7, 10);

const renderer = new THREE.WebGLRenderer({
    antialias: true
});

renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.6));
renderer.setSize(stage.clientWidth, stage.clientHeight);

renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;

renderer.domElement.style.position = "absolute";
renderer.domElement.style.inset = "0";

stage.insertBefore(
    renderer.domElement,
    document.getElementById("hud")
);

// ==================================================
// ILUMINACIÓN
// ==================================================

scene.add(
    new THREE.HemisphereLight(
        0xc5c2ad,
        0x30271c,
        1.25
    )
);

const sun = new THREE.DirectionalLight(
    0xffd6a0,
    2.5
);

sun.position.set(-20, 30, 15);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);

sun.shadow.camera.left = -40;
sun.shadow.camera.right = 40;
sun.shadow.camera.top = 40;
sun.shadow.camera.bottom = -40;

scene.add(sun);

const centerLight = new THREE.PointLight(
    0xc2a16e,
    35,
    40
);

centerLight.position.set(0, 8, 0);
scene.add(centerLight);

// ==================================================
// MATERIALES Y TEXTURAS
// ==================================================

function material(color, roughness = 1, metalness = 0) {
    return new THREE.MeshStandardMaterial({
        color,
        roughness,
        metalness
    });
}

function createTexture(base, colors, count = 12000) {
    const canvas = document.createElement("canvas");
    canvas.width = 512;
    canvas.height = 512;

    const ctx = canvas.getContext("2d");

    ctx.fillStyle = base;
    ctx.fillRect(0, 0, 512, 512);

    for (let i = 0; i < count; i++) {
        ctx.globalAlpha = 0.15 + Math.random() * 0.5;

        ctx.fillStyle =
            colors[Math.floor(Math.random() * colors.length)];

        const size = 1 + Math.random() * 5;

        ctx.fillRect(
            Math.random() * 512,
            Math.random() * 512,
            size,
            size
        );
    }

    ctx.globalAlpha = 1;

    const texture = new THREE.CanvasTexture(canvas);

    texture.colorSpace = THREE.SRGBColorSpace;
    texture.wrapS = THREE.RepeatWrapping;
    texture.wrapT = THREE.RepeatWrapping;

    return texture;
}

const dirtTexture = createTexture(
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

dirtTexture.repeat.set(20, 20);

const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(180, 180),
    new THREE.MeshStandardMaterial({
        map: dirtTexture,
        roughness: 1
    })
);

ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;

scene.add(ground);

const stoneTexture = createTexture(
    "#70664f",
    [
        "#4f493b",
        "#92836a",
        "#5c5545",
        "#a09176",
        "#625a49"
    ]
);

stoneTexture.repeat.set(2, 2);

const stoneMaterial = new THREE.MeshStandardMaterial({
    map: stoneTexture,
    roughness: 1
});

// ==================================================
// COLISIONES DEL ESCENARIO
// ==================================================

const obstacles = [];

function createWall(x, z, width, height, depth, rotation = 0) {
    const mesh = new THREE.Mesh(
        new THREE.BoxGeometry(width, height, depth),
        stoneMaterial
    );

    mesh.position.set(x, height / 2, z);
    mesh.rotation.y = rotation;

    mesh.castShadow = true;
    mesh.receiveShadow = true;

    scene.add(mesh);

    const ex =
        Math.abs(Math.cos(rotation)) * width / 2 +
        Math.abs(Math.sin(rotation)) * depth / 2;

    const ez =
        Math.abs(Math.sin(rotation)) * width / 2 +
        Math.abs(Math.cos(rotation)) * depth / 2;

    obstacles.push({
        minX: x - ex,
        maxX: x + ex,
        minZ: z - ez,
        maxZ: z + ez
    });

    return mesh;
}

function createRuin(x, z, width, height, depth) {
    createWall(x, z, width, height, depth);

    for (let i = 0; i < Math.floor(width / 2); i++) {
        const block = new THREE.Mesh(
            new THREE.BoxGeometry(
                width / Math.floor(width / 2) * 0.85,
                0.35,
                depth * 0.9
            ),
            stoneMaterial
        );

        block.position.set(
            x - width / 2 +
            (i + 0.5) * width / Math.floor(width / 2),
            height + 0.1,
            z
        );

        block.rotation.y = (Math.random() - 0.5) * 0.08;
        block.castShadow = true;

        scene.add(block);
    }
}

// Ruinas
createRuin(-14, -13, 10, 7, 6);
createRuin(14, -16, 11, 9, 6);
createRuin(-16, 14, 10, 8, 7);
createRuin(16, 13, 11, 7, 7);

// Muros exteriores
createWall(-25, 0, 5, 10, 50);
createWall(25, 0, 5, 10, 50);
createWall(0, -29, 50, 10, 5);
createWall(0, 29, 50, 10, 5);

// Muros interiores
createWall(-10, -3, 1, 4, 12);
createWall(10, 3, 1, 4, 12);
createWall(0, -17, 14, 5, 1);
createWall(-18, 7, 8, 4, 1);
createWall(18, -7, 8, 4, 1);

// ==================================================
// SACOS DE ARENA Y CAJAS
// ==================================================

const sackMaterial = material(0x776747);

for (let row = 0; row < 2; row++) {
    for (let i = 0; i < 7; i++) {
        for (const [x, z] of [
            [-7 + i * 1.05, -5],
            [8 + i * 1.05, 6]
        ]) {
            const bag = new THREE.Mesh(
                new THREE.SphereGeometry(0.48, 16, 10),
                sackMaterial
            );

            bag.scale.set(1.25, 0.55, 0.72);

            bag.position.set(
                x,
                0.32 + row * 0.48,
                z + (row % 2) * 0.3
            );

            bag.castShadow = true;
            bag.receiveShadow = true;

            scene.add(bag);
        }
    }
}

const crateMaterial = material(0x494331);

for (let i = 0; i < 12; i++) {
    const crate = new THREE.Mesh(
        new THREE.BoxGeometry(1.1, 0.8, 0.9),
        crateMaterial
    );

    crate.position.set(
        (Math.random() - 0.5) * 34,
        0.4,
        (Math.random() - 0.5) * 34
    );

    crate.rotation.y = Math.random() * Math.PI;
    crate.castShadow = true;
    crate.receiveShadow = true;

    scene.add(crate);
}

// ==================================================
// ESCOMBROS Y ÁRBOLES
// ==================================================

for (let i = 0; i < 150; i++) {
    const rock = new THREE.Mesh(
        new THREE.DodecahedronGeometry(
            0.2 + Math.random() * 0.5
        ),
        material(0x625943)
    );

    rock.position.set(
        (Math.random() - 0.5) * 58,
        0.12,
        (Math.random() - 0.5) * 58
    );

    rock.rotation.set(
        Math.random() * 3,
        Math.random() * 3,
        Math.random() * 3
    );

    rock.castShadow = true;

    scene.add(rock);
}

for (let i = 0; i < 12; i++) {
    const x = (Math.random() - 0.5) * 55;
    const z = (Math.random() - 0.5) * 55;

    if (Math.abs(x) < 10 && Math.abs(z) < 10) continue;

    const trunk = new THREE.Mesh(
        new THREE.CylinderGeometry(0.12, 0.24, 4, 8),
        material(0x30271d)
    );

    trunk.position.set(x, 2, z);
    trunk.castShadow = true;

    scene.add(trunk);

    for (let j = 0; j < 4; j++) {
        const branch = new THREE.Mesh(
            new THREE.CylinderGeometry(0.035, 0.08, 2, 7),
            material(0x30271d)
        );

        branch.position.set(
            x + (Math.random() - 0.5),
            3 + j * 0.15,
            z
        );

        branch.rotation.z = (Math.random() - 0.5) * 1.5;

        scene.add(branch);
    }
}

// ==================================================
// FAROLES
// ==================================================

for (const [x, z] of [
    [-20, -5],
    [20, 5],
    [-19, 20],
    [19, -20]
]) {
    const pole = new THREE.Mesh(
        new THREE.CylinderGeometry(0.08, 0.13, 5, 10),
        material(0x393a34, 0.6, 0.5)
    );

    pole.position.set(x, 2.5, z);
    pole.castShadow = true;

    scene.add(pole);

    const lamp = new THREE.PointLight(0xffb85c, 18, 12);
    lamp.position.set(x, 4.8, z);

    scene.add(lamp);

    const bulb = new THREE.Mesh(
        new THREE.SphereGeometry(0.14, 12, 8),
        new THREE.MeshBasicMaterial({
            color: 0xffd28a
        })
    );

    bulb.position.set(x, 4.8, z);
    scene.add(bulb);
}

// ==================================================
// PARTÍCULAS DE POLVO
// ==================================================

const dustGeometry = new THREE.BufferGeometry();
const dustPositions = new Float32Array(500 * 3);

for (let i = 0; i < 500; i++) {
    dustPositions[i * 3] = (Math.random() - 0.5) * 60;
    dustPositions[i * 3 + 1] = Math.random() * 9;
    dustPositions[i * 3 + 2] = (Math.random() - 0.5) * 60;
}

dustGeometry.setAttribute(
    "position",
    new THREE.BufferAttribute(dustPositions, 3)
);

const dust = new THREE.Points(
    dustGeometry,
    new THREE.PointsMaterial({
        color: 0xd5c49b,
        size: 0.065,
        transparent: true,
        opacity: 0.5
    })
);

scene.add(dust);

// ==================================================
// ARMA EN PRIMERA PERSONA
// ==================================================

const weapon = new THREE.Group();

function weaponPart(geometry, material, x, y, z) {
    const mesh = new THREE.Mesh(geometry, material);

    mesh.position.set(x, y, z);
    mesh.castShadow = true;

    weapon.add(mesh);

    return mesh;
}

const gunMetal = material(0x242722, 0.4, 0.75);
const woodMaterial = material(0x49301e);
const darkMetal = material(0x111310, 0.5, 0.5);

weaponPart(
    new THREE.BoxGeometry(0.22, 0.18, 0.65),
    gunMetal,
    0, 0, 0
);

const barrel = weaponPart(
    new THREE.CylinderGeometry(0.045, 0.055, 0.58, 16),
    darkMetal,
    0, 0.025, -0.48
);

barrel.rotation.x = Math.PI / 2;

const muzzle = weaponPart(
    new THREE.CylinderGeometry(0.065, 0.065, 0.12, 16),
    darkMetal,
    0, 0.025, -0.79
);

muzzle.rotation.x = Math.PI / 2;

weaponPart(
    new THREE.BoxGeometry(0.16, 0.2, 0.32),
    woodMaterial,
    0, -0.025, 0.42
);

weaponPart(
    new THREE.BoxGeometry(0.12, 0.28, 0.15),
    woodMaterial,
    -0.04, -0.19, 0.12
);

weaponPart(
    new THREE.BoxGeometry(0.07, 0.07, 0.12),
    darkMetal,
    0, 0.12, -0.22
);

weaponPart(
    new THREE.BoxGeometry(0.23, 0.25, 0.35),
    material(0x4a4b3c),
    0.12, -0.28, 0.28
);

weapon.position.set(0.36, -0.31, -0.72);

camera.add(weapon);
scene.add(camera);

const muzzleFlash = new THREE.PointLight(
    0xffbd65,
    0,
    5
);

muzzleFlash.position.set(0, 0, -1);
camera.add(muzzleFlash);

// ==================================================
// ESTADO DEL JUEGO
// ==================================================

const game = {
    health: 100,
    score: 0,
    ammo: 12,
    maxAmmo: 12,
    round: 1,
    started: false,
    paused: false,
    over: false,
    reloading: false,
    damageCooldown: 0
};

let zombies = [];
let keys = {};

let spawned = 0;
let spawnTotal = 0;
let spawnClock = 0;

let lastShot = 0;
let recoil = 0;

const clock = new THREE.Clock();
const raycaster = new THREE.Raycaster();

function collides(x, z, radius = 0.42) {
    for (const obstacle of obstacles) {
        const closestX = THREE.MathUtils.clamp(
            x,
            obstacle.minX,
            obstacle.maxX
        );

        const closestZ = THREE.MathUtils.clamp(
            z,
            obstacle.minZ,
            obstacle.maxZ
        );

        const dx = x - closestX;
        const dz = z - closestZ;

        if (dx * dx + dz * dz < radius * radius) {
            return true;
        }
    }

    return false;
}

function movePlayer(dx, dz) {
    const nextX = camera.position.x + dx;
    const nextZ = camera.position.z + dz;

    if (!collides(nextX, camera.position.z)) {
        camera.position.x = nextX;
    }

    if (!collides(camera.position.x, nextZ)) {
        camera.position.z = nextZ;
    }
}

// ==================================================
// ZOMBIS
// ==================================================

function createZombie() {
    const group = new THREE.Group();

    const skin = material(0x68764f);
    const coat = material(0x343b31);
    const pants = material(0x292c26);

    const torso = new THREE.Mesh(
        new THREE.BoxGeometry(0.62, 0.88, 0.36),
        coat
    );

    torso.position.y = 1.12;
    group.add(torso);

    const head = new THREE.Mesh(
        new THREE.SphereGeometry(0.27, 18, 14),
        skin
    );

    head.position.y = 1.76;
    group.add(head);

    const arms = [];
    const legs = [];

    for (const side of [-1, 1]) {
        const eye = new THREE.Mesh(
            new THREE.SphereGeometry(0.04, 8, 8),
            new THREE.MeshBasicMaterial({
                color: 0xffb83e
            })
        );

        eye.position.set(side * 0.095, 1.79, 0.235);
        group.add(eye);

        const arm = new THREE.Mesh(
            new THREE.BoxGeometry(0.19, 0.72, 0.2),
            skin
        );

        arm.position.set(side * 0.42, 1.15, 0.04);
        group.add(arm);
        arms.push(arm);

        const leg = new THREE.Mesh(
            new THREE.BoxGeometry(0.23, 0.68, 0.25),
            pants
        );

        leg.position.set(side * 0.17, 0.38, 0);
        group.add(leg);
        legs.push(leg);
    }

    group.traverse(object => {
        if (object.isMesh) {
            object.castShadow = true;
            object.receiveShadow = true;
        }
    });

    let angle = Math.random() * Math.PI * 2;
    const distance = 22 + Math.random() * 10;

    let x = camera.position.x + Math.cos(angle) * distance;
    let z = camera.position.z + Math.sin(angle) * distance;

    for (let i = 0; i < 25 && collides(x, z, 0.7); i++) {
        angle += 0.45;

        x = camera.position.x + Math.cos(angle) * distance;
        z = camera.position.z + Math.sin(angle) * distance;
    }

    group.position.set(x, 0, z);
    scene.add(group);

    zombies.push({
        mesh: group,
        hp: 1 + Math.floor((game.round - 1) / 4),
        speed: 0.9 + game.round * 0.1,
        cooldown: 0,
        phase: Math.random() * 6,
        arms,
        legs
    });
}

function beginRound() {
    spawnTotal = 5 + game.round * 3;
    spawned = 0;
    spawnClock = 0.5;
}

// ==================================================
// INTERFAZ
// ==================================================

function updateHUD() {
    document.getElementById("round").textContent = game.round;
    document.getElementById("score").textContent = game.score;
    document.getElementById("health").textContent =
        Math.ceil(game.health);

    document.getElementById("ammo").textContent =
        game.reloading
        ? "RECARGANDO"
        : `${game.ammo} / ${game.maxAmmo}`;

    document.getElementById("count").textContent =
        zombies.length + spawnTotal - spawned;
}

function showMenu(message, buttonText) {
    document.getElementById("status").textContent = message;
    document.getElementById("start").textContent = buttonText;
    document.getElementById("overlay").style.display = "flex";
}

function startGame() {
    if (game.over) {
        zombies.forEach(zombie => scene.remove(zombie.mesh));
        zombies = [];

        game.health = 100;
        game.score = 0;
        game.ammo = 12;
        game.round = 1;
        game.over = false;
        game.reloading = false;

        camera.position.set(0, 1.7, 10);
        camera.rotation.set(0, 0, 0);

        spawnTotal = 0;
    }

    game.started = true;
    game.paused = false;

    document.getElementById("overlay").style.display = "none";

    if (spawnTotal === 0) {
        beginRound();
    }

    updateHUD();
}

document.getElementById("start").addEventListener(
    "click",
    startGame
);

// ==================================================
// RECARGAR
// ==================================================

function reload() {
    if (
        !game.started ||
        game.paused ||
        game.reloading ||
        game.ammo === game.maxAmmo
    ) {
        return;
    }

    game.reloading = true;
    updateHUD();

    setTimeout(() => {
        if (game.over) return;

        game.ammo = game.maxAmmo;
        game.reloading = false;

        updateHUD();
    }, 1450);
}

// ==================================================
// DISPARO Y DETECCIÓN DE IMPACTOS
// ==================================================

function shoot() {
    if (
        !game.started ||
        game.paused ||
        game.over ||
        game.reloading ||
        game.ammo <= 0
    ) {
        return;
    }

    const now = performance.now();

    if (now - lastShot < 240) return;

    lastShot = now;
    game.ammo--;

    recoil = 0.1;
    muzzleFlash.intensity = 5;

    setTimeout(() => {
        muzzleFlash.intensity = 0;
    }, 55);

    raycaster.setFromCamera(
        new THREE.Vector2(0, 0),
        camera
    );

    let target = null;
    let nearest = Infinity;

    // Comprobar si una pared bloquea la trayectoria.
    const wallHits = raycaster.intersectObjects(
        scene.children.filter(object =>
            object.isMesh &&
            object !== ground &&
            object !== weapon
        ),
        false
    );

    const firstWallDistance =
        wallHits.length > 0
        ? wallHits[0].distance
        : Infinity;

    for (const zombie of zombies) {
        const center = zombie.mesh.position.clone();
        center.y = 1.15;

        const hit = raycaster.ray.intersectSphere(
            new THREE.Sphere(center, 0.72),
            new THREE.Vector3()
        );

        if (hit) {
            const distance = camera.position.distanceTo(hit);

            if (
                distance < nearest &&
                distance < firstWallDistance
            ) {
                nearest = distance;
                target = zombie;
            }
        }
    }

    if (target) {
        target.hp--;

        if (target.hp <= 0) {
            scene.remove(target.mesh);

            zombies = zombies.filter(
                zombie => zombie !== target
            );

            game.score += 100;
        }
    }

    updateHUD();
}

renderer.domElement.addEventListener("click", () => {
    shoot();
});

// ==================================================
// DAÑO Y ESTADO DE PARTIDA
// ==================================================

function damagePlayer() {
    if (game.damageCooldown > 0) return;

    game.health -= 8;
    game.damageCooldown = 0.9;

    if (game.health <= 0) {
        game.health = 0;
        game.over = true;
        game.started = false;

        showMenu(
            "HAS SIDO DERROTADO · PUNTOS: " + game.score,
            "VOLVER A JUGAR"
        );
    }

    updateHUD();
}

// ==================================================
// MOVIMIENTO Y ANIMACIÓN DE ZOMBIS
// ==================================================

function updateZombies(dt) {
    for (const zombie of zombies) {
        const dx =
            camera.position.x - zombie.mesh.position.x;

        const dz =
            camera.position.z - zombie.mesh.position.z;

        const distance = Math.hypot(dx, dz);

        zombie.phase += dt * 7;

        zombie.arms[0].rotation.x =
            Math.sin(zombie.phase) * 0.45;

        zombie.arms[1].rotation.x =
            -Math.sin(zombie.phase) * 0.45;

        zombie.legs[0].rotation.x =
            Math.sin(zombie.phase) * 0.35;

        zombie.legs[1].rotation.x =
            -Math.sin(zombie.phase) * 0.35;

        if (distance > 1.35) {
            const vx = dx / distance * zombie.speed * dt;
            const vz = dz / distance * zombie.speed * dt;

            const nextX = zombie.mesh.position.x + vx;
            const nextZ = zombie.mesh.position.z + vz;

            if (!collides(nextX, zombie.mesh.position.z, 0.38)) {
                zombie.mesh.position.x = nextX;
            }

            if (!collides(zombie.mesh.position.x, nextZ, 0.38)) {
                zombie.mesh.position.z = nextZ;
            }

            zombie.mesh.rotation.y = Math.atan2(dx, dz);

            zombie.mesh.position.y =
                Math.abs(Math.sin(zombie.phase)) * 0.04;
        } else {
            zombie.cooldown -= dt;

            if (zombie.cooldown <= 0) {
                damagePlayer();
                zombie.cooldown = 0.85;
            }
        }
    }
}

// ==================================================
// MOVIMIENTO DEL JUGADOR
// ==================================================

function updatePlayer(dt) {
    const forward = new THREE.Vector3();

    camera.getWorldDirection(forward);

    forward.y = 0;
    forward.normalize();

    const right = new THREE.Vector3(
        -forward.z,
        0,
        forward.x
    );

    const movement = new THREE.Vector3();

    if (keys.w) movement.add(forward);
    if (keys.s) movement.sub(forward);
    if (keys.d) movement.add(right);
    if (keys.a) movement.sub(right);

    if (movement.lengthSq() > 0) {
        movement.normalize();

        const speed = keys.shift ? 7.2 : 5;

        movePlayer(
            movement.x * speed * dt,
            movement.z * speed * dt
        );
    }

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
}

// ==================================================
// CONTROL DEL TOUCHPAD CORREGIDO
// ==================================================

// El cursor puede moverse normalmente.
// No se usa Pointer Lock ni se necesita mantener clic.

let previousX = null;
let previousY = null;
let previousTime = 0;

const sensitivity = 0.0035;

stage.addEventListener("pointermove", event => {
    if (
        !game.started ||
        game.paused ||
        game.over
    ) {
        return;
    }

    if (event.pointerType === "touch") return;

    const now = performance.now();

    if (
        previousX === null ||
        now - previousTime > 500
    ) {
        previousX = event.clientX;
        previousY = event.clientY;
        previousTime = now;
        return;
    }

    const dx = event.clientX - previousX;
    const dy = event.clientY - previousY;

    // Evitar saltos al volver a entrar al escenario.
    if (
        Math.abs(dx) < 150 &&
        Math.abs(dy) < 150
    ) {
        camera.rotation.y -= dx * sensitivity;
        camera.rotation.x -= dy * sensitivity;

        camera.rotation.x = THREE.MathUtils.clamp(
            camera.rotation.x,
            -1.4,
            1.4
        );
    }

    previousX = event.clientX;
    previousY = event.clientY;
    previousTime = now;
});

stage.addEventListener("pointerleave", () => {
    previousX = null;
    previousY = null;
    previousTime = 0;
});

stage.addEventListener("pointerenter", () => {
    previousX = null;
    previousY = null;
    previousTime = 0;
});

// ==================================================
// TECLADO
// ==================================================

window.addEventListener("keydown", event => {
    const key = event.key.toLowerCase();

    keys[key] = true;

    if (["w", "a", "s", "d", " "].includes(key)) {
        event.preventDefault();
    }

    if (key === "r") {
        reload();
    }

    if (
        key === "escape" &&
        game.started &&
        !game.over
    ) {
        game.paused = true;

        showMenu(
            "PARTIDA PAUSADA",
            "CONTINUAR"
        );
    }
});

window.addEventListener("keyup", event => {
    keys[event.key.toLowerCase()] = false;
});

window.addEventListener("blur", () => {
    keys = {};
});

// ==================================================
// BUCLE PRINCIPAL
// ==================================================

function update(dt) {
    if (
        !game.started ||
        game.paused ||
        game.over
    ) {
        return;
    }

    game.damageCooldown = Math.max(
        0,
        game.damageCooldown - dt
    );

    updatePlayer(dt);

    spawnClock -= dt;

    if (
        spawned < spawnTotal &&
        zombies.length < 14 &&
        spawnClock <= 0
    ) {
        createZombie();

        spawned++;
        spawnClock = 1.2;
    }

    updateZombies(dt);

    if (
        spawned >= spawnTotal &&
        zombies.length === 0
    ) {
        game.round++;
        beginRound();
    }

    recoil = Math.max(0, recoil - dt * 0.8);

    weapon.position.z = -0.72 + recoil;
    weapon.rotation.x = -recoil * 0.7;

    updateHUD();
}

function animate() {
    requestAnimationFrame(animate);

    const dt = Math.min(clock.getDelta(), 0.05);

    update(dt);

    // Movimiento de partículas.
    const positions = dust.geometry.attributes.position;

    for (let i = 0; i < positions.count; i++) {
        positions.array[i * 3 + 1] += 0.001;

        if (positions.array[i * 3 + 1] > 9) {
            positions.array[i * 3 + 1] = 0;
        }
    }

    positions.needsUpdate = true;

    renderer.render(scene, camera);
}

animate();

// ==================================================
// REDIMENSIONAR
// ==================================================

window.addEventListener("resize", () => {
    camera.aspect =
        stage.clientWidth / stage.clientHeight;

    camera.updateProjectionMatrix();

    renderer.setSize(
        stage.clientWidth,
        stage.clientHeight
    );
});

updateHUD();

</script>
</body>
</html>
"""

components.html(html, height=750, scrolling=False)

st.caption("Ejecuta el juego con: python -m streamlit run Juegos.py")
