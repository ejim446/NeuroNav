# NeuroNav

[NeuroNav](https://neuronav.netlify.app/) is a simple web 3D brain atlas built with THREE.js that serves as an anatomical reference for various brain regions. This repository contains the source code for the application.

## Models and Data

All models were adapted from the MRI imaging format of the Allen Human Reference Atlas 3D (2020).

### Dataset Citation

Song‐Lin Ding, Joshua J. Royall, Susan M. Sunkin, Benjamin A.C. Facer, Phil Lesnar, Amy Bernard, Lydia Ng, Ed S. Lein (2020). “Allen Human Reference Atlas – 3D, 2020," RRID:SCR_017764, version 1.0.0.

[Access the dataset here](https://download.alleninstitute.org/informatics-archive/allen_human_reference_atlas_3d_2020/version_1/)

## Getting Started

### Prerequisites

- Node.js
- npm

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ejim446/neuronav.git
   ```
2. Install NPM packages
   ```sh
   npm install
   ```
3. Build the app
   ```sh
   npm run build
   ```
4. Run on local server
   ```sh
   npm run serve
   ``````

## Usage

Open [http://localhost:3000](http://localhost:3000) to view it in your browser. Use the mouse to rotate, zoom, and navigate through the scene.

## Inspiration

This project was inspired by the interactive 3D brain from [BrainFacts.org](https://www.brainfacts.org/3d-brain#intro=true).
