import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { DRACOLoader } from "three/examples/jsm/Addons.js";
import {
  acceleratedRaycast,
  computeBoundsTree,
  disposeBoundsTree,
} from "three-mesh-bvh";

THREE.Mesh.prototype.raycast = acceleratedRaycast;
THREE.BufferGeometry.prototype.computeBoundsTree = computeBoundsTree;
THREE.BufferGeometry.prototype.disposeBoundsTree = disposeBoundsTree;

// SCENE //

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff);

// CAMERA //

const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000,
);
camera.position.set(0, 0, -4);
camera.lookAt(scene.position);

// LIGHTING //

const ambientLight = new THREE.AmbientLight({ intensity: 10000 });
scene.add(ambientLight);

// RENDERER //

const renderer = new THREE.WebGLRenderer({
  canvas: document.querySelector("#bg"),
});

renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);

// CONTROLS //

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.enableZoom = true;

// Controls maximum and minimum zoom distance
controls.minDistance = 1;
controls.maxDistance = 5;
// Ensure models are always centered while panning
controls.maxTargetRadius = 0.5;

const raycaster = new THREE.Raycaster();
raycaster.firstHitOnly = true;
const pointer = new THREE.Vector2();
const pointerClientPosition = { x: 0, y: 0 };
let pointerInsideRenderer = false;
let pointerNeedsTooltipUpdate = false;
const raycastTargets = [];
let raycastTargetsDirty = true;

function markRaycastTargetsDirty() {
  raycastTargetsDirty = true;
}

function rebuildRaycastTargets() {
  raycastTargets.length = 0;
  visibleRegions.forEach((regionName) => {
    const meshes = regionMeshMap.get(regionName);
    if (meshes && meshes.length) {
      raycastTargets.push(...meshes);
    }
  });
  raycastTargetsDirty = false;
}

// WINDOW RESIZE //

window.addEventListener("resize", () => {
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
});

// ANIMATION LOOP //

function animate() {
  requestAnimationFrame(animate);
  controls.update();

  if (pointerNeedsTooltipUpdate) {
    processTooltipRaycast();
  }

  renderer.render(scene, camera);
}

animate();

// OUTLINE EFFECT //

// Flag for toggling outlines
let outlinesEnabled = true;

// Creates an outline for a given mesh by pushing its vertices outward along their normals
function createOutline(mesh, regionName) {
  const THICKNESS = 0.005; // Define outline thickness

  // Clone geometry to avoid modifying original
  const geometry = mesh.geometry.clone();

  if (geometry?.isBufferGeometry) {
    geometry.computeBoundsTree();
  }

  const positionAttribute = geometry.attributes.position;
  if (!positionAttribute) {
    return;
  }

  let normalAttribute = geometry.attributes.normal;
  if (!normalAttribute) {
    geometry.computeVertexNormals();
    normalAttribute = geometry.attributes.normal;
  }

  if (!normalAttribute) {
    return;
  }

  const vertices = positionAttribute.array;
  const normals = normalAttribute.array;

  for (let i = 0; i < vertices.length; i += 3) {
    const nx = normals[i];
    const ny = normals[i + 1];
    const nz = normals[i + 2];
    const normalLength = Math.hypot(nx, ny, nz);

    if (normalLength === 0) {
      continue;
    }

    const scale = THICKNESS / normalLength;
    vertices[i] += nx * scale;
    vertices[i + 1] += ny * scale;
    vertices[i + 2] += nz * scale;
  }

  positionAttribute.needsUpdate = true;

  // Define a fully opaque black material for the outline
  const material = new THREE.ShaderMaterial({
    vertexShader: `
            void main() {
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1);
            }
        `,
    fragmentShader: `
            uniform float uAlpha;
            void main() {
                gl_FragColor = vec4(0, 0, 0, 1);
            }
        `,
    side: THREE.BackSide, // Render the outline on the back side of the mesh
    visible: false, // Initially make the outline invisible
  });

  // Create a new mesh for the outline with the modified geometry and shader material
  const outline = new THREE.Mesh(geometry, material);
  outline.name = `${regionName}Outline`; // Set the name for the outline mesh

  // Add the outline mesh to the scene
  scene.add(outline);
}

// FADE IN EFFECT //

function fadeObject(object, fadeType) {
  const startTime = performance.now();
  const duration = 100;
  const material = object.material;
  if (!material) {
    return;
  }

  const outline = scene.getObjectByName(`${object.name}Outline`);

  function enableFadeState() {
    material.transparent = true;
    material.depthWrite = false;
  }

  function restoreOpaqueState(finalOpacity) {
    material.opacity = finalOpacity;
    material.transparent = false;
    material.depthWrite = true;
  }



  function getProgress() {

    const currentTime = performance.now();

    const elapsed = currentTime - startTime;

    const progress = Math.min(1, elapsed / duration); // Normalize progress to between 0 and 1



    return progress;

  }



  function fadeInMaterial() {
    enableFadeState();
    const progress = getProgress();

    // Show outline and set opacity to normalized [0, 1] progress
    object.visible = true;
    material.visible = true;
    material.opacity = progress;


    if (progress === 1) {
      restoreOpaqueState(1);
      if (outlinesEnabled && outline?.material) {
        outline.material.visible = true;
      }
      return;
    }

    if (progress < 1) {

      requestAnimationFrame(fadeInMaterial); // Fade in until progress == 1

    }

  }



  function fadeOutMaterial() {

    enableFadeState();
    const progress = getProgress();



    // Hide outline and set opacity to inverse of progress
    if (outline?.material) {
      outline.material.visible = false;
    }
    material.opacity = 1 - progress;

    // Update visibility upon zero opacity to avoid artifacts
    if (material.opacity == 0) {
      material.visible = false;
      object.visible = false;
    }


    if (progress < 1) {

      requestAnimationFrame(fadeOutMaterial); // Fade in until progress == 1

    } else {
      restoreOpaqueState(0);
    }

  }



  if (fadeType === "in") {

    fadeInMaterial();

  } else if (fadeType === "out") {

    fadeOutMaterial();

  }

}


/// HANDLE GLB FILES ///

const gltfLoader = new GLTFLoader();
const draco = new DRACOLoader();
draco.setDecoderPath("https://www.gstatic.com/draco/versioned/decoders/1.5.7/");
gltfLoader.setDRACOLoader(draco);

const loadedRegions = new Set();
const visibleRegions = new Set();
const regionMeshMap = new Map();

function addVisibleRegion(regionName) {
  if (!visibleRegions.has(regionName)) {
    visibleRegions.add(regionName);
    markRaycastTargetsDirty();
  }
}

function removeVisibleRegion(regionName) {
  if (visibleRegions.delete(regionName)) {
    markRaycastTargetsDirty();
  }
}

const _addRoot = async () => {
  // Define transparent root material
  const material = new THREE.MeshBasicMaterial({
    color: 0xd3d3d3,
    // Setting depthWrite to false disables occlusion of brain regions by the root mesh
    depthWrite: false,
    transparent: true,
    opacity: 0.15,
  });

  // Load the GLB file
  gltfLoader.load(
    // "/models/root.glb",
    "/models/root.glb",

    function (gltf) {
      gltf.scene.traverse((child) => {
        if (child.isMesh) {
          child.material = material;
          if (child.geometry?.isBufferGeometry) {
            child.geometry.computeBoundsTree();
          }
        }
      });

      scene.add(gltf.scene);
    },
  );
};

_addRoot();

/// REGION SELECTIONS ///

// DEFINE AVAILABLE COLORS //

const colors = {
  Yellow: 0xffec84,
  "Deep Blue": 0x4f55ff,
  Magenta: 0xff79f2,
  Pink: 0xffb6c7,
  Peach: 0xffe0d5,
  Ivory: 0xfff7d9,
  Coral: 0xffa38c,
  "Light Blue": 0xc4d0ff,
};

// LOAD SELECTED //

export function loadRegion(regionID, colorSelection, hemisphereSelection) {
  const loadRegionObject = (regionName) => {
    // Check if the region is already loaded
    if (!loadedRegions.has(regionName)) {
      // Load the GLB model for the region
      gltfLoader.load(`/models/${regionName}.glb`, function (gltf) {
        // Create a material with the selected color
        const material = new THREE.MeshBasicMaterial({
          color: colors[colorSelection],
          transparent: false,
          opacity: 1,
        });

        // Traverse the loaded model
        const meshes = [];
        gltf.scene.traverse((child) => {
          if (child.isMesh) {
            // Ensure the mesh is identifiable by region name
            child.name = regionName;
            // Apply the material to the mesh
            child.material = material;
            if (child.geometry?.isBufferGeometry) {
              child.geometry.computeBoundsTree();
            }
            // Create an outline for the mesh
            createOutline(child, regionName);
            // Fade in the object
            fadeObject(child, "in");
            meshes.push(child);
          }
        });

        if (meshes.length) {
          regionMeshMap.set(regionName, meshes);
        }

        // Add the loaded model to the scene
        scene.add(gltf.scene);
        // Mark the region as loaded and visible
        loadedRegions.add(regionName);
        addVisibleRegion(regionName);
        if (tooltipsEnabled && pointerInsideRenderer) {
          pointerNeedsTooltipUpdate = true;
        }
      });
    } else {
      // If the region is already loaded, just show it
      showRegion(regionName);
    }
  };

  const showRegion = (regionName) => {
    const meshes = regionMeshMap.get(regionName);
    if (!meshes) return;

    meshes.forEach((mesh) => {
      fadeObject(mesh, "in");
    });
    addVisibleRegion(regionName);
    if (tooltipsEnabled && pointerInsideRenderer) {
      pointerNeedsTooltipUpdate = true;
    }
  };

  // Determine which hemisphere(s) to load based on selection
  if (hemisphereSelection === "Both") {
    // Load both left and right hemispheres
    const regionNames = [`${regionID}L`, `${regionID}R`];
    regionNames.forEach(loadRegionObject);
  } else {
    // Load only the selected hemisphere
    const hemisphereSuffix = hemisphereSelection === "Left" ? "L" : "R";
    const regionName = `${regionID}${hemisphereSuffix}`;
    loadRegionObject(regionName);
  }
}

/// HIDE REGIONS ///

// UPON DESELECT //

export function hideRegion(regionID, hemisphereSelection) {
  if (hemisphereSelection === "Both") {
    // If both hemispheres are selected, hide both left and right regions
    ["L", "R"].forEach((suffix) => {
      const regionName = `${regionID}${suffix}`;
      const meshes = regionMeshMap.get(regionName);
      if (!meshes) return;

      meshes.forEach((mesh) => fadeObject(mesh, "out"));
      removeVisibleRegion(regionName);
    });
  } else {
    // If only one hemisphere is selected
    // Determine the correct hemisphere suffix (L for Left, R for Right)
    const hemisphereSuffix = hemisphereSelection === "Left" ? "L" : "R";
    const regionName = `${regionID}${hemisphereSuffix}`;

    const meshes = regionMeshMap.get(regionName);
    if (meshes) {
      meshes.forEach((mesh) => fadeObject(mesh, "out"));
      removeVisibleRegion(regionName);
    }
  }

  hideTooltip();
  if (pointerInsideRenderer && tooltipsEnabled) {
    pointerNeedsTooltipUpdate = true;
  }
}

// DESELECT ALL //

export function hideAll() {
  const regionsToHide = Array.from(visibleRegions);
  regionsToHide.forEach((regionName) => {
    const meshes = regionMeshMap.get(regionName);
    if (!meshes) return;

    meshes.forEach((mesh) => fadeObject(mesh, "out"));
    removeVisibleRegion(regionName);
  });

  hideTooltip();
  pointerNeedsTooltipUpdate = false;
}

// UPDATE COLORS //

export function updateColor(selectedColor, regionID, hemisphereSelection) {
  // Helper function to set the color for a specific region
  const setRegionColor = (regionName) => {
    const meshes = regionMeshMap.get(regionName);
    if (!meshes) return;

    meshes.forEach((mesh) => {
      mesh.material.color.setHex(colors[selectedColor]);
    });
  };

  // Check if both hemispheres are selected
  if (hemisphereSelection === "Both") {
    // If both, update color for both left and right regions
    const regionNames = [`${regionID}L`, `${regionID}R`];
    regionNames.forEach(setRegionColor);
  } else {
    // If not both, determine which hemisphere is selected
    const hemisphereSuffix = hemisphereSelection === "Left" ? "L" : "R";
    const regionName = `${regionID}${hemisphereSuffix}`;
    // Update color for the selected hemisphere
    setRegionColor(regionName);
  }
}

// UPDATE SELECTED HEMISPHERE //

export function updateHemisphere(regionID, hemisphereSelection, selectedColor) {
  // Helper function to load a specific hemisphere
  const loadSelectedHemisphere = (selectedHemisphere) => {
    loadRegion(regionID, selectedColor, selectedHemisphere);
  };

  // Helper function to unload (hide) the opposite hemisphere
  const unloadOppositeHemisphere = (currentHemisphere) => {
    // Determine the opposite hemisphere
    const oppositeHemisphere = currentHemisphere === "Left" ? "Right" : "Left";
    // Hide the opposite hemisphere
    hideRegion(regionID, oppositeHemisphere);
  };

  // Check if a specific hemisphere is selected (Left or Right)
  if (hemisphereSelection === "Left" || hemisphereSelection === "Right") {
    // Load the selected hemisphere
    loadSelectedHemisphere(hemisphereSelection);
    // Unload the opposite hemisphere
    unloadOppositeHemisphere(hemisphereSelection);
  } else {
    // If "Both" is selected, load both hemispheres
    loadSelectedHemisphere("Left");
    loadSelectedHemisphere("Right");
  }
}

/// SETTINGS ///

// HIDE ROOT //

let rootVisible = true; // DEFAULT

export function hideRoot() {
  // Helper function to set visibility of the root object
  const setVisible = (visible) => {
    // Traverse all objects in the scene
    scene.traverse(function (object) {
      // Check if the object is a mesh and named "root"
      if (object instanceof THREE.Mesh && object.name === "root") {
        // Set the visibility of the root object's material
        object.material.visible = visible;
      }
    });
  };

  // Toggle the global rootVisible state
  rootVisible = !rootVisible;

  // Apply the new visibility state to the root object
  setVisible(rootVisible);
}

// TOGGLE REGION OUTLINES //

export function updateOutlines(outlinesSelected) {
  if (outlinesSelected) {
    // If outlines are selected to be shown

    // Set global flag indicating outlines are enabled
    outlinesEnabled = true;

    // Traverse all objects in the scene
    scene.traverse(function (object) {
      // Check if the object is an outline and its corresponding region is visible
      if (
        object.name.includes("Outline") &&
        visibleRegions.has(object.name.slice(0, -7))
      ) {
        // Make the outline visible
        object.material.visible = true;
      }
    });
  } else {
    // If outlines are selected to be hidden

    // Set global flag indicating outlines are disabled
    outlinesEnabled = false;

    // Traverse all objects in the scene
    scene.traverse(function (object) {
      // Check if the object is an outline
      if (object.name.includes("Outline")) {
        // Hide the outline
        object.material.visible = false;
      }
    });
  }
}

// TOGGLE SCENE BACKGROUND //

export function updateBackground() {
  // Get current background color upon function call
  const currentColor = scene.background.getHexString();

  // Set background to opposite
  const targetColor = currentColor === "ffffff" ? 0x000000 : 0xffffff;
  scene.background = new THREE.Color(targetColor);
  return targetColor === 0x000000;
}

/// REGION TOOLTIPS ///

let tooltipsEnabled = true;
let descriptionBoxesEnabled = true;
let hoveredRegionName = null;

// DISABLE TOOLTIPS //

export function disableTooltips(check) {
  if (!check) {
    tooltipsEnabled = false;
    hoveredRegionName = null;
    tooltip.style.display = "none";
  } else {
    tooltipsEnabled = true;
    if (pointerInsideRenderer) {
      pointerNeedsTooltipUpdate = true;
    }
  }
}

export function disableDescriptionBoxes(check) {
  descriptionBoxesEnabled = !check;
  if (!descriptionBoxesEnabled) {
    hideRegionInfoPanel();
  }
}

// Fetch regions data
let regions;
fetch("/reference.json")
  .then((response) => response.json())
  .then((data) => {
    regions = data;
  });

const tooltip = document.createElement("div");

function createTooltipContent(regionInfo) {
  const name = regionInfo.name ?? "";
  const groups = Array.isArray(regionInfo.groups)
    ? regionInfo.groups
    : regionInfo.groups
      ? [regionInfo.groups]
      : [];

  const normalizedGroups = groups
    .map((group) => (typeof group === "string" ? group.trim() : ""))
    .filter(Boolean);

  let content = `<strong>${name}</strong>`;
  if (normalizedGroups.length) {
    content += `<br/><small>${normalizedGroups.join(" • ")}</small>`;
  }
  return content;
}

// Tooltip styling
Object.assign(tooltip.style, {
  position: "absolute",
  display: "none",
  backgroundColor: "rgba(0, 0, 0, 0.7)",
  color: "#fff",
  padding: "5px",
  borderRadius: "5px",
  zIndex: "4",
});

document.body.appendChild(tooltip);

function hideTooltip() {
  hoveredRegionName = null;
  tooltip.style.display = "none";
}

function showTooltip(position, regionObject) {
  if (!tooltipsEnabled || !regionObject) {
    hideTooltip();
    return;
  }

  const regionId = regionObject.name.slice(0, -1);
  const regionInfo = regions && regions[regionId];

  if (hoveredRegionName !== regionObject.name) {
    hoveredRegionName = regionObject.name;
    if (regionInfo) {
      tooltip.innerHTML = createTooltipContent(regionInfo);
    } else {
      tooltip.textContent = regionId;
    }
  }

  tooltip.style.display = "block";
  tooltip.style.left = `${position.x + 10}px`;
  tooltip.style.top = `${position.y + 10}px`;
}

function updatePointerState(event) {
  pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;
  pointerClientPosition.x = event.clientX;
  pointerClientPosition.y = event.clientY;
}

function onPointerMove(event) {
  updatePointerState(event);
  pointerInsideRenderer = true;

  if (tooltipsEnabled) {
    pointerNeedsTooltipUpdate = true;
  }
}

function onPointerLeave() {
  pointerInsideRenderer = false;
  pointerNeedsTooltipUpdate = false;
  hideTooltip();
}

renderer.domElement.addEventListener("pointermove", onPointerMove);
renderer.domElement.addEventListener("pointerleave", onPointerLeave);

function processTooltipRaycast() {
  if (!tooltipsEnabled || !pointerInsideRenderer) {
    pointerNeedsTooltipUpdate = false;
    return;
  }

  const object = getIntersectedRegionFromPointer(pointer);

  if (object && visibleRegions.has(object.name)) {
    showTooltip(pointerClientPosition, object);
  } else {
    hideTooltip();
  }

  pointerNeedsTooltipUpdate = false;
}

const infoPanel = document.getElementById("region-info-panel");

const REGION_INFO_PANEL_WIDTH_DEFAULTS = {
  minRem: 24,
  maxRem: 32,
  stepRem: 1,
};

function parseRemValue(value, fallbackRem) {
  if (typeof value !== "string") {
    return fallbackRem;
  }

  const trimmedValue = value.trim();

  if (!trimmedValue) {
    return fallbackRem;
  }

  const parsed = Number.parseFloat(trimmedValue);

  return Number.isFinite(parsed) ? parsed : fallbackRem;
}

function getRegionInfoPanelWidthSettings() {
  const rootStyle = getComputedStyle(document.documentElement);

  const minRem = parseRemValue(
    rootStyle.getPropertyValue("--region-info-panel-min-width"),
    REGION_INFO_PANEL_WIDTH_DEFAULTS.minRem,
  );

  const maxRem = parseRemValue(
    rootStyle.getPropertyValue("--region-info-panel-max-width"),
    REGION_INFO_PANEL_WIDTH_DEFAULTS.maxRem,
  );

  return {
    minRem,
    maxRem: Math.max(minRem, maxRem),
    stepRem: REGION_INFO_PANEL_WIDTH_DEFAULTS.stepRem,
  };
}

function resetRegionInfoPanelWidth(panel) {
  if (!panel) return;
  panel.style.removeProperty("--region-info-panel-width");
  panel.classList.remove("region-info-panel-scrollable");
}

function adjustRegionInfoPanelWidth(panel) {
  if (!panel) return;

  const { minRem, maxRem, stepRem } = getRegionInfoPanelWidthSettings();
  const rootFontSize = Number.parseFloat(
    getComputedStyle(document.documentElement).fontSize,
  );

  if (!Number.isFinite(rootFontSize) || rootFontSize <= 0) {
    resetRegionInfoPanelWidth(panel);
    return;
  }

  let widthRem = minRem;
  panel.style.setProperty("--region-info-panel-width", `${widthRem}rem`);
  panel.classList.remove("region-info-panel-scrollable");

  // Trigger layout before measuring so the new width takes effect.
  panel.getBoundingClientRect();

  while (panel.scrollHeight > panel.clientHeight && widthRem < maxRem) {
    widthRem = Math.min(widthRem + stepRem, maxRem);
    panel.style.setProperty("--region-info-panel-width", `${widthRem}rem`);
    panel.getBoundingClientRect();
  }

  if (panel.scrollHeight > panel.clientHeight) {
    panel.classList.add("region-info-panel-scrollable");
  } else {
    panel.classList.remove("region-info-panel-scrollable");
  }
}

function escapeHtml(value) {
  if (value == null) {
    return "";
  }
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function escapeAttribute(value) {
  return escapeHtml(value);
}

function normalizeToArray(values) {
  if (!values) return [];
  if (Array.isArray(values)) {
    return values
      .map((value) => (typeof value === "string" ? value.trim() : ""))
      .filter(Boolean);
  }
  if (typeof values === "string") {
    const trimmed = values.trim();
    return trimmed ? [trimmed] : [];
  }
  return [];
}

function linkifyCitations(text, citations) {
  if (typeof text !== "string") {
    return "";
  }

  const trimmedText = text.trim();
  if (!trimmedText) {
    return "";
  }

  const escapedText = escapeHtml(trimmedText);
  if (!Array.isArray(citations) || !citations.length) {
    return escapedText;
  }

  return escapedText.replace(/\[(\d+)\]/g, (match, numberString) => {
    const citationIndex = Number.parseInt(numberString, 10) - 1;
    if (!Number.isInteger(citationIndex) || citationIndex < 0) {
      return match;
    }

    const citation = citations[citationIndex];
    if (typeof citation !== "string") {
      return match;
    }

    const trimmedCitation = citation.trim();
    if (!trimmedCitation) {
      return match;
    }

    const safeHref = escapeAttribute(trimmedCitation);
    const ariaLabel = escapeAttribute(`Reference ${numberString}`);
    return `<a class="region-info-inline-citation" href="${safeHref}" target="_blank" rel="noopener noreferrer" aria-label="${ariaLabel}">[${numberString}]</a>`;
  });
}

function renderInfoList(values, emptyMessage, citations) {
  const items = normalizeToArray(values);
  if (!items.length) {
    return `<p class="region-info-placeholder">${emptyMessage}</p>`;
  }
  return `<ul class="region-info-list">${items
    .map((item) => `<li>${linkifyCitations(item, citations)}</li>`)
    .join("")}</ul>`;
}

function showRegionInfoPanel(regionId, hemisphere, regionInfo) {
  if (!infoPanel) return;

  if (!descriptionBoxesEnabled) {
    hideRegionInfoPanel();
    return;
  }

  const name = regionInfo?.name ?? regionId;
  const description = regionInfo?.description?.trim();
  const alternativeNames =
    regionInfo?.aliases && regionInfo.aliases.length
      ? regionInfo.aliases
      : regionInfo?.keywords;
  const groups = normalizeToArray(regionInfo?.groups);
  const embryonicOrigin =
    typeof regionInfo?.embryonic_origin === "string"
      ? regionInfo.embryonic_origin.trim()
      : "";

  const descriptionSection = description
    ? `<p class="region-info-description">${linkifyCitations(
        description,
        regionInfo?.citations,
      )}</p>`
    : `<p class="region-info-placeholder">No description available.</p>`;

  const embryonicOriginSection = embryonicOrigin
    ? `<div class="region-info-section"><h4>Embryonic Origin</h4><p class="region-info-embryonic-origin">${linkifyCitations(
        embryonicOrigin,
        regionInfo?.citations,
      )}</p></div>`
    : `<div class="region-info-section"><h4>Embryonic Origin</h4><p class="region-info-placeholder">No embryonic origin information available.</p></div>`;

  const groupsSection = groups.length
    ? `<div class="region-info-section"><h4>Groups</h4><p class="region-info-groups">${groups
        .map((group) => escapeHtml(group))
        .join(" • ")}</p></div>`
    : "";

  infoPanel.innerHTML = `
    <h3>${name}</h3>
    <p class="region-info-subtitle">${hemisphere} Hemisphere • ID ${regionId}</p>
    ${descriptionSection}
    ${embryonicOriginSection}
    <div class="region-info-section">
      <h4>Alternative Names</h4>
      ${renderInfoList(
        alternativeNames,
        "No alternative names recorded.",
        regionInfo?.citations,
      )}
    </div>
    <div class="region-info-section">
      <h4>Functions</h4>
      ${renderInfoList(
        regionInfo?.functions,
        "No functional summary available.",
        regionInfo?.citations,
      )}
    </div>
    <div class="region-info-section">
      <h4>Connections</h4>
      ${renderInfoList(
        regionInfo?.connections,
        "No connection data available.",
        regionInfo?.citations,
      )}
    </div>
    ${groupsSection}
  `;

  infoPanel.classList.add("visible");
  infoPanel.setAttribute("aria-hidden", "false");

  adjustRegionInfoPanelWidth(infoPanel);
}

function hideRegionInfoPanel() {
  if (!infoPanel) return;

  infoPanel.classList.remove("visible");
  infoPanel.setAttribute("aria-hidden", "true");
  infoPanel.innerHTML = "";
  resetRegionInfoPanelWidth(infoPanel);
}

if (infoPanel) {
  infoPanel.addEventListener("click", (event) => event.stopPropagation());
  hideRegionInfoPanel();
}

// Event listeners
renderer.domElement.addEventListener("click", onClick);
document.body.addEventListener("click", () => {
  if (tooltipsEnabled) hideTooltip();
  hideRegionInfoPanel();
});

function getIntersectedRegion(event) {
  updatePointerState(event);
  pointerInsideRenderer = true;
  return getIntersectedRegionFromPointer(pointer);
}

function getIntersectedRegionFromPointer(pointerVector) {
  if (!visibleRegions.size) return null;

  if (raycastTargetsDirty) {
    rebuildRaycastTargets();
  }

  if (!raycastTargets.length) return null;

  raycaster.setFromCamera(pointerVector, camera);
  const intersects = raycaster.intersectObjects(raycastTargets, false);

  if (!intersects.length) return null;

  for (let i = 0; i < intersects.length; i++) {
    const candidate = intersects[i].object;
    const candidateName = candidate.name;

    if (candidate instanceof THREE.Mesh && visibleRegions.has(candidateName)) {
      return candidate;
    }
  }

  return null;
}

function onClick(event) {
  const object = getIntersectedRegion(event);

  if (object && visibleRegions.has(object.name)) {
    const regionId = object.name.slice(0, -1);
    const hemisphere = object.name.endsWith("L")
      ? "Left"
      : object.name.endsWith("R")
        ? "Right"
        : "Midline";
    const regionInfo = regions && regions[regionId];

    showRegionInfoPanel(regionId, hemisphere, regionInfo);

    if (tooltipsEnabled) {
      showTooltip({ x: event.clientX, y: event.clientY }, object);
    } else {
      hideTooltip();
    }

    event.stopPropagation();
  } else {
    if (tooltipsEnabled) {
      hideTooltip();
    }
    hideRegionInfoPanel();
  }
}
