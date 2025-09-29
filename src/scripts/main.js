import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { DRACOLoader } from "three/examples/jsm/Addons.js";

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

// WINDOW RESIZE //

window.addEventListener("resize", () => {
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
});

// ANIMATION LOOP //

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
  controls.update();
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
  // geometry.applyMatrix4(mesh.matrixWorld); // Ensure object transformations are reflected in geometry

  // Get vertices and normals arrays
  const vertices = geometry.attributes.position.array;
  const normals = geometry.attributes.normal.array;

  // Modify the vertices by pushing them outward along their normals, i += 3 used to specify x, y, z
  for (let i = 0; i < vertices.length; i += 3) {
    // Create vectors for the current vertex and its normal
    const vertex = new THREE.Vector3(
      vertices[i],
      vertices[i + 1],
      vertices[i + 2],
    );
    const normal = new THREE.Vector3(
      normals[i],
      normals[i + 1],
      normals[i + 2],
    ).normalize();

    // Push the vertex outward by the thickness amount
    vertex.addScaledVector(normal, THICKNESS);

    // Update the vertices array with the new vertex position
    vertices[i] = vertex.x;
    vertices[i + 1] = vertex.y;
    vertices[i + 2] = vertex.z;
  }

  // Update geometry with the modified vertices
  geometry.setAttribute("position", new THREE.BufferAttribute(vertices, 3));

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

  // Define startTime upon function call

  const startTime = performance.now();



  // Fade in duration in ms

  const duration = 100;



  // Get material to fade and corresponding outline

  const material = object.material;

  const outline = scene.getObjectByName(`${object.name}Outline`);



  function getProgress() {

    const currentTime = performance.now();

    const elapsed = currentTime - startTime;

    const progress = Math.min(1, elapsed / duration); // Normalize progress to between 0 and 1



    return progress;

  }



  function fadeInMaterial() {
    const progress = getProgress();

    // Show outline and set opacity to normalized [0, 1] progress
    object.visible = true;
    material.visible = true;
    material.opacity = progress;


    if (progress == 1 && outlinesEnabled) {

      outline.material.visible = true;

    }

    if (progress < 1) {

      requestAnimationFrame(fadeInMaterial); // Fade in until progress == 1

    }

  }



  function fadeOutMaterial() {

    const progress = getProgress();



    // Hide outline and set opacity to inverse of progress
    outline.material.visible = false;
    material.opacity = 1 - progress;

    // Update visibility upon zero opacity to avoid artifacts
    if (material.opacity == 0) {
      material.visible = false;
      object.visible = false;
    }


    if (progress < 1) {

      requestAnimationFrame(fadeOutMaterial); // Fade in until progress == 1

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
          transparent: true,
          opacity: 1,
        });

        // Traverse the loaded model
        gltf.scene.traverse((child) => {
          if (child.isMesh) {
            // Apply the material to the mesh
            child.material = material;
            // Create an outline for the mesh
            createOutline(child, regionName);
            // Fade in the object
            fadeObject(child, "in");
          }
        });

        // Add the loaded model to the scene
        scene.add(gltf.scene);
        // Mark the region as loaded and visible
        loadedRegions.add(regionName);
        visibleRegions.add(regionName);
      });
    } else {
      // If the region is already loaded, just show it
      showRegion(regionName);
    }
  };

  const showRegion = (regionName) => {
    // Traverse the scene to find the region object
    scene.traverse(function (object) {
      if (object instanceof THREE.Mesh && object.name === `${regionName}`) {
        // Fade in the object
        fadeObject(object, "in");
        // Mark the region as visible
        visibleRegions.add(regionName);
      }
    });
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
    scene.traverse(function (object) {
      // Check if the object is a mesh and matches either left or right region ID
      if (
        object instanceof THREE.Mesh &&
        (object.name === `${regionID}L` || object.name === `${regionID}R`)
      ) {
        // Fade out the object (and outline)
        fadeObject(object, "out");

        // Remove the region from the list of visible regions
        visibleRegions.delete(object.name);
      }
    });
  } else {
    // If only one hemisphere is selected
    // Determine the correct hemisphere suffix (L for Left, R for Right)
    const hemisphereSuffix = hemisphereSelection === "Left" ? "L" : "R";
    const regionName = `${regionID}${hemisphereSuffix}`;

    // Traverse the scene to find the specific region to hide
    scene.traverse(function (object) {
      if (object instanceof THREE.Mesh && object.name === regionName) {
        // Fade out the object
        fadeObject(object, "out");

        // Remove the region from the list of visible regions
        visibleRegions.delete(regionName);
      }
    });
  }
}

// DESELECT ALL //

export function hideAll() {
  // Traverse all objects in the scene
  scene.traverse(function (object) {
    // Check if the object is a mesh, not the root object, and not an outline (removed in fadeObject)
    if (
      object instanceof THREE.Mesh &&
      object.name !== "root" &&
      !object.name.includes("Outline")
    ) {
      // Fade out the object
      fadeObject(object, "out");

      // Remove the object from the list of visible regions
      visibleRegions.delete(object.name);
    }
  });
}

// UPDATE COLORS //

export function updateColor(selectedColor, regionID, hemisphereSelection) {
  // Helper function to set the color for a specific region
  const setRegionColor = (regionName) => {
    // Traverse all objects in the scene
    scene.traverse(function (object) {
      // Check if the object is a mesh and matches the region name
      if (object instanceof THREE.Mesh && object.name === regionName) {
        // Update the color of the object's material
        object.material.color.setHex(colors[selectedColor]);
      }
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

// DISABLE TOOLTIPS //

export function disableTooltips(check) {
  if (!check) {
    tooltipsEnabled = false;
    tooltip.style.display = "none";
  } else {
    tooltipsEnabled = true;
  }
}

// Fetch regions data
let regions;
fetch("/reference.json")
  .then((response) => response.json())
  .then((data) => {
    regions = data;
  });

const raycaster = new THREE.Raycaster();
const tooltip = document.createElement("div");

function createTooltipContent(regionInfo) {
  const name = regionInfo.name ?? "";
  const related = Array.from(
    new Set([...(regionInfo.groups ?? []), ...(regionInfo.keywords ?? [])]),
  ).filter((value) => value && value.toLowerCase() !== name.toLowerCase());
  const description = regionInfo.description?.trim();

  let content = `<strong>${name}</strong>`;
  if (related.length) {
    content += `<br/><small>${related.slice(0, 3).join(" • ")}</small>`;
  }
  if (description) {
    content += `<br/>${description}`;
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

// Event listeners
renderer.domElement.addEventListener("click", onClick);
document.body.addEventListener("click", () => {
  if (tooltipsEnabled) tooltip.style.display = "none";
});

function onClick(event) {
  if (!tooltipsEnabled) return; // Do nothing if tooltips are disabled

  // Find coordinates of the mouse position
  const mouse = new THREE.Vector2(
    (event.clientX / window.innerWidth) * 2 - 1,
    -(event.clientY / window.innerHeight) * 2 + 1,
  );

  // Update the raycaster with the mouse coordinates and the camera
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(scene.children, true); // Get all intersected objects

  if (intersects.length > 0) {
    let object; // Initialize variable to hold the intersected object
    try {
      // Loop through the intersected objects
      for (let i = 0; i < intersects.length; i++) {
        const candidate = intersects[i].object;
        const candidateName = candidate.name;

        const isRegionMesh =
          candidate instanceof THREE.Mesh &&
          candidateName !== "root" &&
          !candidateName.includes("Outline");

        // Check if the object is a valid, currently visible region
        if (isRegionMesh && visibleRegions.has(candidateName)) {
          object = candidate; // Assign the first valid object
          break; // Exit the loop once a valid object is found
        }
      }
    } catch (error) {
      object = undefined; // Catch empty intersects
    }

    // If a valid object is found and it is visible
    if (object && visibleRegions.has(object.name)) {
      // Set the tooltip content to the region name
      const regionId = object.name.slice(0, -1);
      const regionInfo = regions && regions[regionId];
      if (regionInfo) {
        tooltip.innerHTML = createTooltipContent(regionInfo);
      } else {
        tooltip.innerHTML = regionId;
      }
      // Display the tooltip and position it near the mouse cursor
      tooltip.style.display = "block";
      tooltip.style.left = `${event.clientX + 10}px`;
      tooltip.style.top = `${event.clientY + 10}px`;
      event.stopPropagation(); // Stop event propagation to prevent other click handlers
    } else {
      tooltip.style.display = "none"; // Hide the tooltip if no valid object is found
    }
  } else {
    tooltip.style.display = "none"; // Hide the tooltip if no intersections are found
  }
}
