import json
from pathlib import Path

updates = {
    "3": {
        "description": "Primary olfactory cortex that interprets odor information relayed from the olfactory bulb.",
        "aliases": [
            "Piriform area",
            "Pyriform cortex"
        ],
        "functions": [
            "Generates sparse ensembles that encode odor identity and intensity.",
            "Supports associative olfactory memory and rapid odor discrimination."
        ],
        "connections": [
            "Receives lateral olfactory tract input from mitral and tufted cells of the olfactory bulb.",
            "Projects to the orbitofrontal cortex, amygdala, and entorhinal cortex for higher order odor evaluation."
        ]
    },
    "4": {
        "description": "Frontal sector of the insular cortex lacking a granular layer and integrating viscerosensory and limbic signals.",
        "aliases": [
            "Anterior agranular insula",
            "Frontal agranular insula"
        ],
        "functions": [
            "Integrates autonomic, gustatory, and interoceptive cues with emotional context.",
            "Contributes to vocalization, taste perception, and affective decision making."
        ],
        "connections": [
            "Interconnected with the anterior cingulate cortex and orbitofrontal cortex for salience processing.",
            "Receives thalamic input from the ventromedial posterior nucleus conveying visceral afferents."
        ]
    },
    "5": {
        "description": "Temporal subdivision of agranular insular cortex bridging olfactory and limbic networks.",
        "aliases": [
            "Temporal agranular insula",
            "Agranular insular area TI"
        ],
        "functions": [
            "Processes multimodal sensory cues tied to taste, olfaction, and internal bodily state.",
            "Participates in emotional memory formation and autonomic regulation."
        ],
        "connections": [
            "Reciprocal connections with the amygdala and entorhinal cortex via the temporal pole.",
            "Receives visceral sensory input from the parabrachial nucleus through the thalamus."
        ]
    },
    "6": {
        "description": "Anterior portion of the caudate nucleus involved in goal-directed action selection and cognitive control.",
        "aliases": [
            "Caudate head",
            "Caput nuclei caudati"
        ],
        "functions": [
            "Supports working memory, planning, and reward-based learning with prefrontal circuits.",
            "Evaluates action-outcome contingencies during flexible behavior."
        ],
        "connections": [
            "Receives glutamatergic projections from dorsolateral prefrontal and orbitofrontal cortex.",
            "Sends inhibitory output to the globus pallidus externus and substantia nigra pars reticulata."
        ]
    },
    "7": {
        "description": "Elongated central segment of the caudate nucleus influencing associative motor learning.",
        "aliases": [
            "Caudate body"
        ],
        "functions": [
            "Modulates cortico-basal ganglia loops for habit formation and motor sequence learning.",
            "Integrates sensory context with motor plans from parietal and premotor areas."
        ],
        "connections": [
            "Interconnected with association cortices including parietal and temporal regions via corticostriatal fibers.",
            "Projects through the indirect basal ganglia pathway to the globus pallidus externus."
        ]
    },
    "8": {
        "description": "Posterior tapering portion of the caudate nucleus linked to visual and mnemonic association networks.",
        "aliases": [
            "Caudate tail"
        ],
        "functions": [
            "Supports visuospatial attention and eye movement control with parietal circuits.",
            "Participates in reinforcement learning tied to contextual memory cues."
        ],
        "connections": [
            "Receives input from visual association cortices and the hippocampal formation.",
            "Sends inhibitory projections to the globus pallidus and substantia nigra pars reticulata."
        ]
    },
    "9": {
        "description": "Lateral striatal nucleus central to execution of habitual and sensorimotor behaviors.",
        "aliases": [
            "Putamen nucleus"
        ],
        "functions": [
            "Encodes learned motor programs and stimulus-response associations.",
            "Integrates somatosensory feedback to refine movement vigor and timing."
        ],
        "connections": [
            "Receives dense corticostriatal input from primary motor, premotor, and somatosensory cortices.",
            "Outputs via the globus pallidus internus and substantia nigra pars reticulata to thalamic motor relays."
        ]
    },
    "10": {
        "description": "Key component of the ventral striatum involved in reward and motivation.",
        "aliases": [
            "Ventral striatum",
            "NAc"
        ],
        "functions": [
            "Integrates dopaminergic reward prediction signals with cortical inputs to drive goal-directed behavior.",
            "Mediates reinforcement learning and the hedonic impact of stimuli."
        ],
        "connections": [
            "Receives glutamatergic input from prefrontal cortex, hippocampus, and amygdala.",
            "Projects to ventral pallidum, hypothalamus, and midbrain dopaminergic nuclei."
        ]
    },
    "11": {
        "description": "Lateral division of the globus pallidus that modulates basal ganglia activity through the indirect pathway.",
        "aliases": [
            "GPe",
            "Globus pallidus externus"
        ],
        "functions": [
            "Provides tonic inhibition that shapes subthalamic nucleus excitability.",
            "Contributes to action suppression and timing within cortico-basal ganglia circuits."
        ],
        "connections": [
            "Receives inhibitory input from striatal medium spiny neurons of the indirect pathway.",
            "Projects to the subthalamic nucleus and globus pallidus internus."
        ]
    },
    "12": {
        "description": "Medial output segment of the globus pallidus providing inhibitory drive to thalamocortical motor loops.",
        "aliases": [
            "GPi",
            "Globus pallidus internus"
        ],
        "functions": [
            "Conveys the final basal ganglia inhibitory output that gates movement initiation.",
            "Encodes movement parameters including amplitude and posture."
        ],
        "connections": [
            "Receives convergent input from the striatum and subthalamic nucleus.",
            "Projects to the ventral anterior and ventrolateral thalamic nuclei and to the brainstem."
        ]
    },
    "13": {
        "description": "Thin subcortical sheet coordinating cross-modal integration between cortex and limbic structures.",
        "aliases": [
            "Claustral complex"
        ],
        "functions": [
            "Synchronizes activity across distributed cortical areas during conscious perception.",
            "Mediates multimodal sensory binding and attentional switching."
        ],
        "connections": [
            "Reciprocally connected with nearly all association cortices via extreme capsule fibers.",
            "Links with the amygdala and hippocampal formation through limbic fiber tracts."
        ]
    },
    "14": {
        "description": "Collection of cholinergic and GABAergic nuclei at the base of the forebrain supporting arousal and learning.",
        "aliases": [
            "Basal nucleus complex",
            "Basal forebrain cholinergic system"
        ],
        "functions": [
            "Provides acetylcholine to cerebral cortex and hippocampus to modulate attention and plasticity.",
            "Coordinates sleep-wake transitions and mnemonic encoding."
        ],
        "connections": [
            "Receives input from limbic structures including amygdala and hippocampus.",
            "Projects broadly to neocortex via the medial forebrain bundle and to the hippocampal formation."
        ]
    },
    "15": {
        "description": "Medial basal forebrain nuclei linking limbic circuitry with autonomic and reward systems.",
        "aliases": [
            "Septal area",
            "Septum pellucidum nuclei"
        ],
        "functions": [
            "Regulates hippocampal theta oscillations critical for learning and navigation.",
            "Integrates reward, autonomic, and endocrine signals for motivational states."
        ],
        "connections": [
            "Receives afferents from hippocampus, amygdala, and brainstem monoaminergic nuclei.",
            "Projects via the fornix to hippocampus and hypothalamus, and via the medial forebrain bundle to midbrain tegmentum."
        ]
    },
    "16": {
        "description": "Hub for processing emotional salience and associative memory.",
        "aliases": [
            "Amygdala",
            "Amygdaloid complex"
        ],
        "functions": [
            "Evaluates sensory stimuli for emotional relevance and threat.",
            "Supports consolidation of emotional and social memories."
        ],
        "connections": [
            "Receives multimodal input from sensory cortices, thalamus, and hippocampus.",
            "Projects to hypothalamus, brainstem autonomic centers, and prefrontal cortex."
        ]
    },
    "17": {
        "description": "Anterior transitional zone of the amygdala interfacing olfactory, cortical, and basal forebrain inputs.",
        "aliases": [
            "Anterior amygdaloid area",
            "AAA"
        ],
        "functions": [
            "Integrates olfactory cues with emotional salience signals.",
            "Participates in autonomic adjustments to affective stimuli."
        ],
        "connections": [
            "Receives projections from the olfactory bulb and piriform cortex via the lateral olfactory tract.",
            "Projects to the bed nucleus of the stria terminalis and hypothalamus for autonomic control."
        ]
    },
    "18": {
        "description": "Medial amygdalar output complex governing autonomic and behavioral fear responses.",
        "aliases": [
            "Central amygdaloid nucleus",
            "CeA"
        ],
        "functions": [
            "Coordinates autonomic and endocrine components of conditioned fear.",
            "Controls defensive behaviors and pain modulation."
        ],
        "connections": [
            "Receives input from basolateral amygdala and brainstem nociceptive pathways.",
            "Projects to hypothalamic, midbrain periaqueductal gray, and autonomic brainstem nuclei."
        ]
    },
    "19": {
        "description": "Principal sensory gateway of the amygdala relaying polymodal inputs to associative nuclei.",
        "aliases": [
            "Lateral amygdaloid nucleus",
            "La"
        ],
        "functions": [
            "Forms conditioned stimulus associations during fear and reward learning.",
            "Integrates auditory, visual, and somatosensory cues with affective value."
        ],
        "connections": [
            "Receives sensory thalamic and cortical projections, notably from auditory cortex.",
            "Projects to basolateral and central amygdaloid nuclei to drive emotional responses."
        ]
    },
    "20": {
        "description": "Part of the basolateral complex supporting emotional learning.",
        "aliases": [
            "Basolateral amygdaloid nucleus",
            "BLA"
        ],
        "functions": [
            "Encodes associations between sensory cues and reinforcement outcomes.",
            "Influences decision making through interactions with prefrontal cortex."
        ],
        "connections": [
            "Receives cortical input from temporal, insular, and prefrontal areas.",
            "Projects to central amygdala, nucleus accumbens, and hippocampus."
        ]
    },
    "21": {
        "description": "Transitional amygdalar nucleus linking olfactory and visceral information streams.",
        "aliases": [
            "Basomedial amygdaloid nucleus",
            "Accessory basal nucleus"
        ],
        "functions": [
            "Integrates olfactory, visceral, and contextual information for emotional behavior.",
            "Modulates social and reproductive behaviors via hypothalamic circuits."
        ],
        "connections": [
            "Receives inputs from olfactory cortex, hippocampus, and medial amygdala.",
            "Projects to hypothalamus, bed nucleus of the stria terminalis, and entorhinal cortex."
        ]
    },
    "22": {
        "description": "Olfactory-linked cortical nucleus of the amygdala sampling pheromonal and visceral information.",
        "aliases": [
            "Anterior cortical amygdaloid nucleus"
        ],
        "functions": [
            "Integrates olfactory social cues with limbic valuation pathways.",
            "Supports contextual memory for odor-associated experiences."
        ],
        "connections": [
            "Receives olfactory bulb and piriform cortex projections.",
            "Projects to medial amygdala, bed nucleus of the stria terminalis, and hypothalamic autonomic centers."
        ]
    },
    "23": {
        "description": "Posterior cortical amygdalar subdivision relaying chemosensory inputs to hippocampal circuits.",
        "aliases": [
            "Posterior cortical amygdaloid nucleus"
        ],
        "functions": [
            "Links olfactory cues with spatial and contextual memory systems.",
            "Contributes to emotional modulation of entorhinal-hippocampal pathways."
        ],
        "connections": [
            "Receives inputs from accessory olfactory bulb and temporal association cortex.",
            "Projects to entorhinal cortex and hippocampal formation via the amygdalohippocampal pathway."
        ]
    },
    "24": {
        "description": "Medial amygdalar nucleus processing social odors and coordinating reproductive behaviors.",
        "aliases": [
            "Medial amygdaloid nucleus",
            "MeA"
        ],
        "functions": [
            "Evaluates pheromonal signals relevant to mating and aggression.",
            "Interfaces olfactory information with hypothalamic endocrine control."
        ],
        "connections": [
            "Receives dense projections from accessory olfactory bulb and bed nucleus of the accessory olfactory tract.",
            "Projects to hypothalamic medial preoptic and ventromedial nuclei to regulate reproductive behaviors."
        ]
    },
    "26": {
        "description": "Extended amygdala nucleus coordinating sustained threat responses and stress integration.",
        "aliases": [
            "BNST",
            "Bed nucleus of the stria terminalis"
        ],
        "functions": [
            "Mediates anxiety-like states and prolonged fear responses.",
            "Integrates hormonal and autonomic signals related to stress."
        ],
        "connections": [
            "Receives afferents from amygdala, hippocampus, and prefrontal cortex.",
            "Projects to hypothalamus and brainstem autonomic nuclei through the stria terminalis."
        ]
    },
    "25": {
        "description": "Interface between amygdala and hippocampal formation.",
        "aliases": [
            "Amygdalohippocampal transition area"
        ],
        "functions": [
            "Links emotional valence with contextual and spatial memory processing.",
            "Integrates olfactory inputs with hippocampal encoding of environments."
        ],
        "connections": [
            "Receives afferents from basomedial amygdala and entorhinal cortex.",
            "Projects to hippocampus, subiculum, and hypothalamic nuclei."
        ]
    },
    "27": {
        "description": "Paired diencephalic structure relaying and modulating nearly all ascending sensory and motor information to cortex.",
        "aliases": [
            "Dorsal thalamus"
        ],
        "functions": [
            "Acts as the principal gateway to the cerebral cortex for sensory and associative signals.",
            "Synchronizes cortical oscillations during sleep, attention, and cognition."
        ],
        "connections": [
            "Receives inputs from spinal cord, brainstem, cerebellum, basal ganglia, and limbic structures.",
            "Projects topographically to virtually all cortical areas via thalamocortical fibers."
        ]
    },
    "28": {
        "description": "Anterior thalamic nuclei involved in limbic memory circuits and spatial navigation.",
        "aliases": [
            "Anterior thalamic nuclei",
            "ATN"
        ],
        "functions": [
            "Supports episodic memory consolidation within the Papez circuit.",
            "Contributes to head-direction signaling and spatial orientation."
        ],
        "connections": [
            "Receives inputs from mammillary bodies via the mammillothalamic tract and from hippocampus via the fornix.",
            "Projects to cingulate gyrus and retrosplenial cortex through anterior thalamic radiation."
        ]
    },
    "29": {
        "description": "Thalamic nucleus linking limbic structures with parietal association cortex for spatial processing.",
        "aliases": [
            "Lateral dorsal thalamic nucleus",
            "LD nucleus"
        ],
        "functions": [
            "Facilitates visuospatial attention and navigation.",
            "Integrates hippocampal contextual signals with parietal cortex."
        ],
        "connections": [
            "Receives afferents from hippocampal formation and retrosplenial cortex.",
            "Projects to superior parietal lobule and cingulate cortex."
        ]
    },
    "30": {
        "description": "Mediodorsal thalamic nucleus supporting executive function and emotional regulation.",
        "aliases": [
            "MD nucleus",
            "Dorsomedial thalamic nucleus"
        ],
        "functions": [
            "Mediates working memory and decision making through reciprocal prefrontal interactions.",
            "Integrates limbic inputs for affective appraisal and goal selection."
        ],
        "connections": [
            "Receives input from amygdala, basal ganglia, and olfactory structures.",
            "Projects densely to prefrontal cortex via the anterior thalamic radiation."
        ]
    },
    "31": {
        "description": "Midline thalamic nucleus bridging hippocampal and medial prefrontal networks.",
        "aliases": [
            "Nucleus reuniens",
            "Reuniens nucleus"
        ],
        "functions": [
            "Supports hippocampal-prefrontal synchrony during working memory and consolidation.",
            "Mediates communication between limbic and executive circuits in goal-directed behavior."
        ],
        "connections": [
            "Receives afferents from hippocampus, entorhinal cortex, and hypothalamus.",
            "Projects to medial prefrontal cortex, hippocampus, and subiculum."
        ]
    },
    "32": {
        "description": "Posterior thalamic relay conveying somatosensory and nociceptive information to parietal cortex.",
        "aliases": [
            "Posterolateral thalamic nucleus",
            "PoL"
        ],
        "functions": [
            "Transmits multimodal body sensation including proprioception to associative areas.",
            "Contributes to integration of pain, touch, and movement signals."
        ],
        "connections": [
            "Receives spinothalamic and lemniscal inputs as well as superior colliculus projections.",
            "Projects to posterior parietal cortex and secondary somatosensory cortex."
        ]
    },
    "33": {
        "description": "Visual thalamic nucleus integrating attention and sensory signals.",
        "aliases": [
            "Pulvinar nucleus",
            "Pulvinar"
        ],
        "functions": [
            "Modulates cortico-cortical communication during visual attention.",
            "Integrates visual, auditory, and somatosensory information for orienting."
        ],
        "connections": [
            "Receives input from superior colliculus and visual cortices.",
            "Projects to parietal, temporal, and prefrontal association areas."
        ]
    },
    "34": {
        "description": "Motor-associated thalamic nucleus relaying basal ganglia signals to premotor cortex.",
        "aliases": [
            "Ventral anterior nucleus",
            "VA nucleus"
        ],
        "functions": [
            "Participates in movement initiation and planning via premotor loops.",
            "Modulates motor set and readiness in response to basal ganglia output."
        ],
        "connections": [
            "Receives afferents from globus pallidus internus and substantia nigra pars reticulata.",
            "Projects primarily to premotor cortex and supplementary motor area."
        ]
    },
    "36": {
        "description": "Somatosensory thalamic relay conveying body touch and proprioceptive information to cortex.",
        "aliases": [
            "VPL",
            "Ventral posterolateral nucleus"
        ],
        "functions": [
            "Relays discriminative touch, vibration, and limb position signals from the body.",
            "Supports somatotopic mapping of the contralateral trunk and limbs in S1."
        ],
        "connections": [
            "Receives dorsal column-medial lemniscus and spinothalamic tract inputs.",
            "Projects to primary somatosensory cortex via the posterior limb of the internal capsule."
        ]
    },
    "37": {
        "description": "Thalamic relay for trigeminal and gustatory sensory information destined for face representation.",
        "aliases": [
            "VPM",
            "Ventral posteromedial nucleus"
        ],
        "functions": [
            "Conveys touch, pain, and taste signals from the face and oral cavity to cortex.",
            "Supports thalamocortical integration for speech articulation and facial sensation."
        ],
        "connections": [
            "Receives trigeminothalamic and solitariothalamic projections.",
            "Projects to face area of primary somatosensory cortex and the gustatory insula."
        ]
    },
    "38": {
        "description": "Primary visual thalamic nucleus delivering retinal information to occipital cortex.",
        "aliases": [
            "Dorsal LGN",
            "Lateral geniculate nucleus"
        ],
        "functions": [
            "Processes spatial and chromatic visual signals for conscious perception.",
            "Maintains retinotopic maps and regulates gain via corticothalamic feedback."
        ],
        "connections": [
            "Receives segregated retinal ganglion cell inputs and superior colliculus modulation.",
            "Projects via the optic radiation to primary visual cortex (V1)."
        ]
    },
    "39": {
        "description": "Auditory thalamic nuclei relaying sound information to auditory cortex.",
        "aliases": [
            "Medial geniculate body",
            "MGB"
        ],
        "functions": [
            "Analyzes auditory frequency, intensity, and temporal patterns.",
            "Mediates attentional gating and multimodal integration for auditory stimuli."
        ],
        "connections": [
            "Receives ascending input from inferior colliculus and auditory brainstem nuclei.",
            "Projects to primary and secondary auditory cortices via the acoustic radiation."
        ]
    },
    "40": {
        "description": "Intralaminar thalamic nucleus regulating arousal and motor attention.",
        "aliases": [
            "Centromedian nucleus",
            "CM nucleus"
        ],
        "functions": [
            "Provides diffuse thalamocortical activation that modulates attention and wakefulness.",
            "Influences basal ganglia circuits implicated in motor initiation."
        ],
        "connections": [
            "Receives afferents from brainstem reticular formation, cerebellum, and globus pallidus.",
            "Projects broadly to striatum and widespread cortical regions."
        ]
    },
    "41": {
        "description": "Intralaminar thalamic nucleus participating in nociceptive processing and basal ganglia modulation.",
        "aliases": [
            "Parafascicular nucleus",
            "PF nucleus"
        ],
        "functions": [
            "Conveys pain-related and arousal signals to striatum and cortex.",
            "Supports executive control by interfacing prefrontal cortex with basal ganglia."
        ],
        "connections": [
            "Receives input from spinothalamic pathways, brainstem reticular formation, and cerebellum.",
            "Projects to caudate-putamen, subthalamic nucleus, and frontal cortical areas."
        ]
    },
    "42": {
        "description": "Epithalamic nuclei linking limbic forebrain with midbrain monoaminergic centers.",
        "aliases": [
            "Habenula",
            "Habenular complex"
        ],
        "functions": [
            "Processes negative reward prediction and aversive learning signals.",
            "Modulates circadian rhythms and autonomic responses via brainstem projections."
        ],
        "connections": [
            "Receives afferents from limbic stria medullaris fibers arising in septum, basal forebrain, and hypothalamus.",
            "Projects through the fasciculus retroflexus to interpeduncular nucleus and midbrain dopaminergic nuclei."
        ]
    },
    "43": {
        "description": "Midline epithalamic endocrine organ secreting melatonin and synchronizing circadian rhythms.",
        "aliases": [
            "Pineal gland",
            "Epiphysis cerebri"
        ],
        "functions": [
            "Releases melatonin to signal night length and regulate sleep-wake cycles.",
            "Modulates seasonal reproductive and metabolic adaptations."
        ],
        "connections": [
            "Receives sympathetic innervation from the superior cervical ganglion via the hypothalamus.",
            "Communicates with hypothalamic suprachiasmatic nucleus through hormonal feedback loops."
        ]
    },
    "44": {
        "description": "Heterogeneous subthalamic zone that modulates sensorimotor, limbic, and arousal circuits.",
        "aliases": [
            "Field of Forel",
            "Zona incerta nucleus"
        ],
        "functions": [
            "Integrates somatosensory and proprioceptive signals for motor coordination.",
            "Influences arousal, feeding, and whisking behaviors through widespread projections."
        ],
        "connections": [
            "Receives inputs from cortex, cerebellum, and superior colliculus.",
            "Projects to thalamus, brainstem reticular formation, and spinal cord."
        ]
    },
    "45": {
        "description": "Lens-shaped nucleus of the subthalamus critical for indirect basal ganglia pathway control.",
        "aliases": [
            "STN",
            "Subthalamic body"
        ],
        "functions": [
            "Provides excitatory drive to globus pallidus internus and substantia nigra pars reticulata.",
            "Regulates movement suppression and scaling within basal ganglia loops."
        ],
        "connections": [
            "Receives inhibitory projections from globus pallidus externus and cortical hyperdirect inputs.",
            "Projects glutamatergic axons to globus pallidus, substantia nigra, and pedunculopontine nucleus."
        ]
    },
    "46": {
        "description": "Diencephalic control center coordinating endocrine, autonomic, and behavioral responses.",
        "aliases": [
            "Hypothalamus"
        ],
        "functions": [
            "Maintains homeostasis by regulating temperature, hunger, thirst, and circadian rhythms.",
            "Controls pituitary hormone release and integrates stress and reproductive responses."
        ],
        "connections": [
            "Receives input from limbic forebrain, retina, and visceral sensory pathways.",
            "Projects to pituitary gland, brainstem autonomic nuclei, and widespread limbic regions."
        ]
    },
    "47": {
        "description": "Hypothalamic region anterior to the optic chiasm coordinating thermoregulation and reproductive behavior.",
        "aliases": [
            "Preoptic area",
            "POA"
        ],
        "functions": [
            "Monitors body temperature and initiates heat dissipation responses.",
            "Regulates gonadotropin release and parental behaviors via hormone control."
        ],
        "connections": [
            "Receives input from limbic forebrain, retina, and visceral sensory pathways.",
            "Projects to hypothalamic endocrine nuclei, autonomic brainstem centers, and spinal cord."
        ]
    },
    "48": {
        "description": "Hypothalamic zone surrounding the supraoptic nucleus involved in fluid balance and circadian control.",
        "aliases": [
            "Supraoptic region"
        ],
        "functions": [
            "Produces vasopressin and oxytocin for osmotic regulation and parturition.",
            "Integrates retinal light input to influence circadian rhythms."
        ],
        "connections": [
            "Receives direct retinal projections via the retinohypothalamic tract and visceral sensory feedback.",
            "Projects to posterior pituitary via the hypothalamo-neurohypophyseal tract and to brainstem autonomic nuclei."
        ]
    },
    "49": {
        "description": "Hypothalamic tuberal zone housing the arcuate, ventromedial, and dorsomedial nuclei for metabolic control.",
        "aliases": [
            "Tuberal hypothalamus"
        ],
        "functions": [
            "Monitors nutrient and hormone signals to regulate appetite and energy expenditure.",
            "Coordinates neuroendocrine outputs for growth, stress, and circadian rhythms."
        ],
        "connections": [
            "Receives visceral and hormonal inputs via the median eminence and vagal pathways.",
            "Projects to pituitary portal system, autonomic brainstem centers, and limbic cortex."
        ]
    },
    "50": {
        "description": "Posterior hypothalamic region containing mammillary bodies for memory and autonomic functions.",
        "aliases": [
            "Mammillary hypothalamus"
        ],
        "functions": [
            "Supports recollective memory via participation in the Papez circuit.",
            "Regulates arousal and autonomic responses to emotional stimuli."
        ],
        "connections": [
            "Receives hippocampal inputs through the fornix.",
            "Projects to anterior thalamic nuclei via the mammillothalamic tract and to tegmental nuclei."
        ]
    },
    "51": {
        "description": "Composite of major myelinated fiber pathways interconnecting forebrain regions.",
        "aliases": [
            "Forebrain white matter"
        ],
        "functions": [
            "Supports rapid communication between cortical, subcortical, and limbic structures.",
            "Provides structural scaffolding for large-scale functional networks."
        ],
        "connections": [
            "Contains association, commissural, and projection fibers linking cerebral hemispheres.",
            "Integrates cortical processing with thalamus, basal ganglia, and brainstem targets."
        ]
    },
    "52": {
        "description": "Compact commissural fiber bundle interconnecting the temporal lobes and olfactory cortices.",
        "aliases": [
            "Anterior commissural bundle"
        ],
        "functions": [
            "Facilitates bilateral integration of olfactory and temporal lobe information.",
            "Supports interhemispheric transfer for amygdalar and temporal associative processing."
        ],
        "connections": [
            "Connects anterior temporal neocortex, olfactory bulbs, and amygdaloid nuclei across hemispheres.",
            "Links basal forebrain structures and contributes fibers to the stria medullaris thalami."
        ]
    },
    "53": {
        "description": "Major commissural tract joining homologous cortical areas across the cerebral hemispheres.",
        "aliases": [
            "Callosal commissure"
        ],
        "functions": [
            "Enables interhemispheric integration of sensory, motor, and cognitive information.",
            "Supports bilateral coordination of movement and higher cognition."
        ],
        "connections": [
            "Contains fibers from virtually all neocortical regions organized topographically.",
            "Connects cingulate, frontal, parietal, temporal, and occipital cortices between hemispheres."
        ]
    },
    "54": {
        "description": "C-shaped limbic tract linking hippocampus with septal nuclei and mammillary bodies.",
        "aliases": [
            "Fornical commissure"
        ],
        "functions": [
            "Transmits hippocampal output involved in memory consolidation.",
            "Coordinates hippocampal activity with hypothalamic and septal structures."
        ],
        "connections": [
            "Arises from hippocampal subiculum and CA1 pyramidal neurons.",
            "Projects to mammillary bodies, septal nuclei, and anterior thalamic nuclei."
        ]
    },
    "55": {
        "description": "Prominent limbic fiber tract conveying mammillary body signals to anterior thalamus.",
        "aliases": [
            "Vicq d’Azyr bundle"
        ],
        "functions": [
            "Carries memory-related information within the Papez circuit.",
            "Synchronizes hippocampal and thalamic activity during recollection."
        ],
        "connections": [
            "Originates in the medial mammillary nucleus.",
            "Terminates in anterior thalamic nuclei with collaterals to tegmental regions."
        ]
    },
    "56": {
        "description": "Continuation of the optic nerve conveying retinal output to thalamic and midbrain targets.",
        "aliases": [
            "Postchiasmatic optic pathway"
        ],
        "functions": [
            "Transfers visual signals for conscious perception and reflexive eye movements.",
            "Provides collateral input for circadian and pupillary responses."
        ],
        "connections": [
            "Carries axons from retinal ganglion cells to lateral geniculate nucleus, superior colliculus, and pretectum.",
            "Gives off fibers to suprachiasmatic nucleus for circadian entrainment."
        ]
    },
    "57": {
        "description": "Frontal horn of the lateral ventricle containing cerebrospinal fluid adjacent to the head of the caudate.",
        "aliases": [
            "Anterior lateral ventricle horn"
        ],
        "functions": [
            "Serves as a CSF reservoir buffering pressure changes in the frontal lobe.",
            "Provides ventricular landmarks for neurosurgical navigation."
        ],
        "connections": [
            "Continuous with the body of the lateral ventricle posteriorly.",
            "Communicates with the inferior horn via the ventricular atrium and with the third ventricle via the interventricular foramen."
        ]
    },
    "58": {
        "description": "Central portion of the lateral ventricle overlying the thalamus and body of the caudate.",
        "aliases": [
            "Lateral ventricle body"
        ],
        "functions": [
            "Circulates cerebrospinal fluid produced by the choroid plexus.",
            "Acts as anatomical corridor for commissural and projection fibers."
        ],
        "connections": [
            "Extends between anterior and posterior horns of the lateral ventricle.",
            "Communicates inferiorly with the temporal horn through the atrium."
        ]
    },
    "59": {
        "description": "Occipital horn of the lateral ventricle extending into the occipital lobe.",
        "aliases": [
            "Posterior lateral ventricle horn"
        ],
        "functions": [
            "Maintains CSF flow to posterior brain regions.",
            "Provides imaging landmark for optic radiation and tapetum."
        ],
        "connections": [
            "Continuous anteriorly with the ventricular atrium and body.",
            "Closely associated with splenial fibers of the corpus callosum and calcar avis."
        ]
    },
    "60": {
        "description": "Temporal horn of the lateral ventricle coursing through the medial temporal lobe.",
        "aliases": [
            "Inferior lateral ventricle horn"
        ],
        "functions": [
            "Conducts CSF alongside the hippocampal formation.",
            "Serves as surgical access route to mesial temporal structures."
        ],
        "connections": [
            "Opens posteriorly into the ventricular atrium and body.",
            "Borders the hippocampus, amygdala, and choroid fissure along its course."
        ]
    },
    "61": {
        "description": "Midline cleft between thalami forming part of the ventricular system.",
        "aliases": [
            "Third cerebral ventricle"
        ],
        "functions": [
            "Distributes cerebrospinal fluid between lateral and fourth ventricles.",
            "Provides access for neuroendocrine communication across hypothalamic walls."
        ],
        "connections": [
            "Receives CSF from lateral ventricles via interventricular foramina of Monro.",
            "Drains into the cerebral aqueduct leading to the fourth ventricle."
        ]
    },
    "62": {
        "description": "Midline cerebellar structure coordinating axial posture.",
        "aliases": [
            "Cerebellar vermis"
        ],
        "functions": [
            "Maintains balance and posture through control of trunk and proximal muscles.",
            "Synchronizes eye movements and vestibular reflexes."
        ],
        "connections": [
            "Receives spinocerebellar and vestibular input and Purkinje cell projections from vermal cortex.",
            "Projects via fastigial nucleus to vestibular nuclei, reticular formation, and thalamus."
        ]
    },
    "63": {
        "description": "Set of intrinsic cerebellar nuclei that constitute the primary output of the cerebellar cortex.",
        "aliases": [
            "Dentate-interposed-fastigial nuclei"
        ],
        "functions": [
            "Transmit processed cerebellar information for coordination of movement and balance.",
            "Modulate motor learning and timing via projections to motor and premotor centers."
        ],
        "connections": [
            "Receive inhibitory Purkinje cell input from cerebellar cortex zones.",
            "Project to red nucleus, thalamus, vestibular nuclei, and reticular formation."
        ]
    },
    "64": {
        "description": "Myelinated fiber system of the hindbrain connecting cerebellum, medulla, and spinal cord.",
        "aliases": [
            "Hindbrain white matter"
        ],
        "functions": [
            "Supports bidirectional communication between cerebellum and brainstem nuclei.",
            "Transmits ascending sensory and descending motor information through the medulla."
        ],
        "connections": [
            "Includes cerebellar peduncles, corticospinal tracts, and ascending sensory pathways.",
            "Links hindbrain structures with spinal cord, cerebellum, and higher brain centers."
        ]
    },
    "65": {
        "description": "Bundle of fibers carrying olfactory bulb output toward cortical olfactory areas.",
        "aliases": [
            "Tractus olfactorius"
        ],
        "functions": [
            "Transmits odor information for conscious perception and limbic processing.",
            "Conveys modulatory feedback from anterior olfactory nucleus to the bulb."
        ],
        "connections": [
            "Arises from mitral and tufted cell axons leaving the olfactory bulb.",
            "Projects to olfactory tubercle, piriform cortex, amygdala, and entorhinal cortex."
        ]
    },
    "66": {
        "description": "Primary motor cortex gyrus controlling contralateral voluntary movements.",
        "aliases": [
            "M1",
            "Brodmann area 4"
        ],
        "functions": [
            "Encodes muscle force and direction for skilled movements.",
            "Supports motor learning through corticospinal plasticity."
        ],
        "connections": [
            "Receives input from premotor, supplementary motor, and somatosensory cortices.",
            "Projects via corticospinal and corticobulbar tracts to spinal and cranial motor nuclei."
        ]
    },
    "67": {
        "description": "Dorsal frontal lobe gyrus involved in self-referential thought and working memory.",
        "aliases": [
            "Superior frontal cortex"
        ],
        "functions": [
            "Supports executive control, attention, and prospective planning.",
            "Contributes to default mode network activity and introspection."
        ],
        "connections": [
            "Interconnected with medial prefrontal, parietal, and cingulate regions.",
            "Projects to premotor cortex, caudate nucleus, and thalamic association nuclei."
        ]
    },
    "68": {
        "description": "Lateral frontal gyrus mediating executive functions and language working memory.",
        "aliases": [
            "Middle frontal cortex",
            "Brodmann areas 9/46"
        ],
        "functions": [
            "Maintains and manipulates information in working memory.",
            "Guides complex decision making and attentional control."
        ],
        "connections": [
            "Receives parietal and temporal association inputs for multimodal integration.",
            "Projects to basal ganglia, mediodorsal thalamus, and premotor areas."
        ]
    },
    "70": {
        "description": "Opercular division of inferior frontal gyrus involved in speech articulation and sensorimotor integration.",
        "aliases": [
            "Pars opercularis",
            "Brodmann area 44"
        ],
        "functions": [
            "Coordinates articulatory planning within Broca’s complex.",
            "Integrates auditory feedback for phonological processing."
        ],
        "connections": [
            "Receives superior temporal gyrus and inferior parietal inputs via the arcuate fasciculus.",
            "Projects to premotor cortex, supplementary motor area, and basal ganglia speech circuits."
        ]
    },
    "71": {
        "description": "Medial frontal gyrus adjacent to olfactory sulcus associated with reward and social valuation.",
        "aliases": [
            "Straight gyrus",
            "Gyrus rectus"
        ],
        "functions": [
            "Processes reward value and emotional salience of stimuli.",
            "Supports social cognition and autobiographical memory retrieval."
        ],
        "connections": [
            "Receives input from orbitofrontal cortex, amygdala, and hippocampus.",
            "Projects to ventromedial prefrontal cortex and hypothalamic autonomic centers."
        ]
    },
    "72": {
        "description": "Medial orbital gyrus contributing to valuation, olfaction, and autonomic control.",
        "aliases": [
            "Medial orbitofrontal gyrus"
        ],
        "functions": [
            "Computes reward expectations and adaptive decision making.",
            "Integrates visceral, gustatory, and olfactory cues."
        ],
        "connections": [
            "Receives sensory input from olfactory and gustatory cortices via orbitofrontal networks.",
            "Projects to hypothalamus, amygdala, and ventral striatum."
        ]
    },
    "73": {
        "description": "Anterior intermediate orbital gyrus bridging medial and lateral orbitofrontal cortex.",
        "aliases": [
            "Anterior intermediate orbital sulcus gyrus"
        ],
        "functions": [
            "Evaluates changing reward contingencies for flexible behavior.",
            "Links sensory valuation with autonomic responses."
        ],
        "connections": [
            "Receives multimodal input from temporal pole, insula, and amygdala.",
            "Projects to ventromedial prefrontal and striatal decision networks."
        ]
    },
    "74": {
        "description": "Posterior intermediate orbital gyrus integrating sensory evidence for adaptive choices.",
        "aliases": [
            "Posterior intermediate orbitofrontal gyrus"
        ],
        "functions": [
            "Tracks reward history and updates behavioral strategies.",
            "Contributes to affective evaluation of social cues."
        ],
        "connections": [
            "Receives inputs from anterior temporal, insular, and cingulate cortices.",
            "Projects to dorsal striatum and medial prefrontal decision-making circuits."
        ]
    },
    "75": {
        "description": "Lateral orbital gyrus participating in sensory integration and inhibitory control.",
        "aliases": [
            "Lateral orbitofrontal cortex"
        ],
        "functions": [
            "Evaluates punishment and negative feedback to guide behavior.",
            "Integrates taste, smell, and somatosensory cues for flavor perception."
        ],
        "connections": [
            "Receives gustatory and somatosensory inputs via the insula and thalamus.",
            "Projects to amygdala, ventral striatum, and dorsolateral prefrontal cortex."
        ]
    },
    "76": {
        "description": "Anterior segment of the paracentral lobule housing supplementary motor representations.",
        "aliases": [
            "Rostral paracentral cortex"
        ],
        "functions": [
            "Controls lower limb and pelvic motor functions alongside supplementary motor areas.",
            "Contributes to bimanual coordination and gait planning."
        ],
        "connections": [
            "Receives input from premotor cortex, cingulate motor areas, and thalamic motor nuclei.",
            "Projects to corticospinal pathways targeting lumbosacral spinal cord."
        ]
    },
    "77": {
        "description": "Frontal opercular region covering the insula and supporting language and gustatory processing.",
        "aliases": [
            "Opercular frontal cortex"
        ],
        "functions": [
            "Facilitates integration of somatosensory and gustatory signals during oral movements.",
            "Participates in speech production and phonological encoding."
        ],
        "connections": [
            "Connected with insula, inferior parietal lobule, and superior temporal gyrus via perisylvian pathways.",
            "Projects to ventral premotor cortex, basal ganglia, and thalamic relays for articulatory control."
        ]
    },
    "78": {
        "description": "Primary somatosensory cortex gyrus processing tactile and proprioceptive information.",
        "aliases": [
            "Postcentral cortex",
            "Brodmann areas 3,1,2"
        ],
        "functions": [
            "Maps contralateral body sensation with high spatial resolution.",
            "Integrates tactile input for object recognition and motor feedback."
        ],
        "connections": [
            "Receives thalamic input from ventral posterior nuclei.",
            "Projects to secondary somatosensory cortex, posterior parietal areas, and motor cortex."
        ]
    },
    "79": {
        "description": "Dorsal parietal lobule supporting sensorimotor integration and spatial attention.",
        "aliases": [
            "Superior parietal lobule"
        ],
        "functions": [
            "Combines visual and somatosensory cues for reaching and grasping.",
            "Maintains representations of body position in space."
        ],
        "connections": [
            "Interconnected with premotor cortex via dorsal stream pathways.",
            "Receives input from visual motion areas and primary somatosensory cortex."
        ]
    },
    "80": {
        "description": "Parietal gyrus involved in phonological processing, praxis, and empathy.",
        "aliases": [
            "Supramarginal gyrus",
            "SMG"
        ],
        "functions": [
            "Supports phonological working memory during language comprehension.",
            "Integrates tactile, visual, and auditory signals for tool use and social cognition."
        ],
        "connections": [
            "Receives input from superior temporal language areas and somatosensory cortex.",
            "Projects to inferior frontal gyrus via the arcuate fasciculus and to premotor cortex."
        ]
    },
    "81": {
        "description": "Angular gyrus forming part of the inferior parietal lobule for semantic processing.",
        "aliases": [
            "Gyrus angularis"
        ],
        "functions": [
            "Integrates multimodal information for language semantics and number cognition.",
            "Contributes to episodic memory retrieval and theory of mind."
        ],
        "connections": [
            "Connected with temporal lobe language networks and hippocampal formation.",
            "Projects to prefrontal cortex and posterior cingulate via long association tracts."
        ]
    },
    "82": {
        "description": "Medial parietal region supporting visuospatial imagery and default-mode activity.",
        "aliases": [
            "Precuneus"
        ],
        "functions": [
            "Participates in visuospatial imagery, self-reflection, and episodic memory.",
            "Coordinates sensorimotor integration for coordinated movement."
        ],
        "connections": [
            "Connected with posterior cingulate, medial frontal cortex, and hippocampal formation.",
            "Receives visual input from occipital cortex and projects to parietal association areas."
        ]
    },
    "83": {
        "description": "Posterior segment of paracentral lobule representing lower limb somatosensory cortex.",
        "aliases": [
            "Caudal paracentral lobule"
        ],
        "functions": [
            "Processes tactile and proprioceptive information from the contralateral leg.",
            "Assists in sensorimotor integration for locomotion."
        ],
        "connections": [
            "Receives thalamic input from ventral posterolateral nucleus.",
            "Projects to supplementary motor area and spinal cord via corticospinal pathways."
        ]
    },
    "84": {
        "description": "Superior temporal lobe gyrus encompassing primary auditory cortex and language areas.",
        "aliases": [
            "STG"
        ],
        "functions": [
            "Processes auditory perception and speech prosody.",
            "Supports social cognition through superior temporal sulcus networks."
        ],
        "connections": [
            "Receives auditory thalamic input from medial geniculate body.",
            "Projects to frontal and parietal language cortices via arcuate and superior longitudinal fasciculi."
        ]
    },
    "85": {
        "description": "Middle temporal gyrus involved in semantic memory, motion perception, and language.",
        "aliases": [
            "MTG"
        ],
        "functions": [
            "Supports lexical retrieval and narrative comprehension.",
            "Processes visual motion cues and social perception."
        ],
        "connections": [
            "Receives input from visual motion area MT/V5 and auditory association cortex.",
            "Projects to inferior frontal gyrus and angular gyrus via middle longitudinal fasciculus."
        ]
    },
    "86": {
        "description": "Inferior temporal gyrus implicated in object recognition and high-level visual processing.",
        "aliases": [
            "ITG"
        ],
        "functions": [
            "Processes complex visual features including faces and scenes.",
            "Supports semantic categorization and visual memory."
        ],
        "connections": [
            "Receives ventral stream input from occipital cortex and fusiform gyrus.",
            "Projects to anterior temporal lobe, amygdala, and orbitofrontal cortex."
        ]
    },
    "87": {
        "description": "Temporal fusiform gyrus mediating high-level visual recognition and language mapping.",
        "aliases": [
            "Fusiform gyrus",
            "Occipitotemporal gyrus"
        ],
        "functions": [
            "Supports face and word form recognition within ventral visual stream.",
            "Contributes to semantic memory and orthographic processing."
        ],
        "connections": [
            "Receives input from inferior occipital and lingual gyri.",
            "Projects to anterior temporal pole, hippocampus, and inferior frontal language areas."
        ]
    },
    "88": {
        "description": "Heschl’s transverse temporal gyrus housing primary auditory cortex.",
        "aliases": [
            "Transverse temporal gyrus",
            "Heschl’s gyrus"
        ],
        "functions": [
            "Performs initial cortical processing of sound frequency and intensity.",
            "Supports temporal resolution for speech perception."
        ],
        "connections": [
            "Receives tonotopic projections from medial geniculate body.",
            "Projects to superior temporal and parietal auditory association areas."
        ]
    },
    "89": {
        "description": "Posterior superior temporal plane important for language lateralization and auditory integration.",
        "aliases": [
            "Planum temporale"
        ],
        "functions": [
            "Supports phonological analysis and speech comprehension.",
            "Integrates auditory spatial cues for sound localization."
        ],
        "connections": [
            "Interconnected with inferior parietal lobule and inferior frontal gyrus via dorsal language pathway.",
            "Receives input from auditory cortex and multimodal superior temporal sulcus regions."
        ]
    },
    "90": {
        "description": "Anterior temporal pole involved in social-emotional processing and semantic memory.",
        "aliases": [
            "Temporal pole cortex",
            "Brodmann area 38"
        ],
        "functions": [
            "Integrates multimodal semantic representations of people and objects.",
            "Mediates emotional valence and social knowledge."
        ],
        "connections": [
            "Receives input from amygdala, orbitofrontal cortex, and temporal association areas.",
            "Projects to limbic structures, ventromedial prefrontal cortex, and temporal language networks."
        ]
    },
    "91": {
        "description": "Anterior portion of the superior temporal plane mediating auditory association and tonotopic mapping.",
        "aliases": [
            "Planum polare"
        ],
        "functions": [
            "Processes complex acoustic patterns and pitch relationships.",
            "Contributes to language prosody and music perception."
        ],
        "connections": [
            "Receives projections from Heschl’s gyrus and auditory belt areas.",
            "Projects to anterior superior temporal sulcus and inferior frontal cortex."
        ]
    },
    "92": {
        "description": "Posterior-most region of the occipital lobe containing primary visual cortex.",
        "aliases": [
            "Occipital apex"
        ],
        "functions": [
            "Supports high-acuity vision and initial cortical processing of visual input.",
            "Maintains retinotopic maps for central visual field."
        ],
        "connections": [
            "Receives input from lateral geniculate nucleus via optic radiations.",
            "Projects to extrastriate visual areas in occipital and temporal lobes."
        ]
    },
    "93": {
        "description": "Medial occipital gyrus forming part of primary visual cortex processing lower visual field.",
        "aliases": [
            "Cuneus cortex"
        ],
        "functions": [
            "Analyzes motion and spatial features from contralateral inferior visual field.",
            "Contributes to visuospatial attention and saccade planning."
        ],
        "connections": [
            "Receives inputs from lateral geniculate nucleus and superior colliculus.",
            "Projects to parietal dorsal stream areas and frontal eye fields."
        ]
    },
    "94": {
        "description": "Medial occipitotemporal gyrus processing upper visual field and complex visual patterns.",
        "aliases": [
            "Lingual gyrus"
        ],
        "functions": [
            "Participates in visual memory, word recognition, and scene analysis.",
            "Integrates visual input with limbic and parahippocampal regions."
        ],
        "connections": [
            "Receives input from primary visual cortex and pulvinar.",
            "Projects to parahippocampal gyrus, fusiform gyrus, and retrosplenial cortex."
        ]
    },
    "95": {
        "description": "Inferior occipitotemporal gyrus contributing to object and face processing.",
        "aliases": [
            "Occipital fusiform gyrus"
        ],
        "functions": [
            "Supports recognition of complex visual stimuli and color perception.",
            "Links early visual processing with temporal semantic networks."
        ],
        "connections": [
            "Receives ventral stream input from V1 and V2.",
            "Projects to anterior fusiform, inferior temporal cortex, and orbitofrontal areas."
        ]
    },
    "96": {
        "description": "Lateral occipital gyrus processing motion, depth, and object contours.",
        "aliases": [
            "Inferior occipital gyrus"
        ],
        "functions": [
            "Supports shape recognition and visual motion perception.",
            "Provides input for facial recognition networks."
        ],
        "connections": [
            "Receives input from primary and secondary visual cortices.",
            "Projects to fusiform gyrus, superior temporal sulcus, and parietal visual areas."
        ]
    },
    "98": {
        "description": "Anterior cingulate gyrus regulating emotion, autonomic function, and cognitive control.",
        "aliases": [
            "ACC",
            "Brodmann areas 24/32"
        ],
        "functions": [
            "Monitors conflict and error to adjust behavior.",
            "Integrates visceral responses with motivational states."
        ],
        "connections": [
            "Receives input from thalamic midline nuclei, amygdala, and prefrontal cortex.",
            "Projects to prefrontal cortex, limbic structures, and brainstem autonomic nuclei."
        ]
    },
    "99": {
        "description": "Posterior cingulate gyrus central to default-mode processing and memory retrieval.",
        "aliases": [
            "PCC",
            "Brodmann areas 23/31"
        ],
        "functions": [
            "Supports autobiographical memory and spatial orientation.",
            "Integrates internal mentation with attentional shifts."
        ],
        "connections": [
            "Receives input from medial temporal lobe and thalamic nuclei.",
            "Projects to precuneus, medial prefrontal cortex, and retrosplenial cortex."
        ]
    },
    "100": {
        "description": "Isthmus linking posterior cingulate and parahippocampal gyri within the limbic lobe.",
        "aliases": [
            "Cinguloparahippocampal isthmus"
        ],
        "functions": [
            "Facilitates information flow between default mode and hippocampal memory circuits.",
            "Supports contextual memory retrieval and visuospatial navigation."
        ],
        "connections": [
            "Receives input from posterior cingulate and retrosplenial cortices.",
            "Projects to parahippocampal gyrus and hippocampal formation."
        ]
    },
    "101": {
        "description": "Medial frontal gyrus below the corpus callosum associated with limbic and olfactory processing.",
        "aliases": [
            "Subcallosal area",
            "Parolfactory gyrus"
        ],
        "functions": [
            "Modulates mood and reward-guided decision making.",
            "Integrates olfactory cues with emotional valence."
        ],
        "connections": [
            "Receives projections from orbitofrontal cortex and amygdala.",
            "Projects to hypothalamus, ventral striatum, and medial prefrontal cortex."
        ]
    },
    "102": {
        "description": "Anterior segment of parahippocampal gyrus interfacing entorhinal cortex with temporal pole.",
        "aliases": [
            "Anterior parahippocampal cortex"
        ],
        "functions": [
            "Supports object-context associations and emotional memory.",
            "Integrates olfactory and visceral signals with hippocampal inputs."
        ],
        "connections": [
            "Receives input from amygdala, piriform cortex, and temporal association areas.",
            "Projects to entorhinal cortex, hippocampus, and orbitofrontal cortex."
        ]
    },
    "103": {
        "description": "Posterior parahippocampal gyrus contributing to scene perception and episodic memory.",
        "aliases": [
            "Posterior parahippocampal cortex"
        ],
        "functions": [
            "Encodes contextual details of places and events.",
            "Supports navigation and visuospatial memory."
        ],
        "connections": [
            "Receives visual input from lingual and fusiform gyri.",
            "Projects to retrosplenial cortex, hippocampus, and entorhinal cortex."
        ]
    },
    "104": {
        "description": "Medial temporal gyrus bordering the hippocampal fissure integrating olfactory and limbic signals.",
        "aliases": [
            "Ambiens gyrus",
            "Gyrus ambiens"
        ],
        "functions": [
            "Participates in olfactory-limbic associative processing.",
            "Serves as transitional cortex between amygdala and hippocampus."
        ],
        "connections": [
            "Receives input from amygdala, entorhinal cortex, and olfactory areas.",
            "Projects to hippocampal formation and orbitofrontal cortex."
        ]
    },
    "105": {
        "description": "Anterior hippocampal segment specialized for emotional memory and stress modulation.",
        "aliases": [
            "Hippocampal head",
            "Pes hippocampi"
        ],
        "functions": [
            "Encodes episodic memories with strong affective content.",
            "Modulates hypothalamic-pituitary-adrenal axis responses."
        ],
        "connections": [
            "Receives input from entorhinal cortex, amygdala, and olfactory structures.",
            "Projects via the fornix to septal nuclei and hypothalamus."
        ]
    },
    "106": {
        "description": "Intermediate hippocampal segment supporting spatial navigation and memory consolidation.",
        "aliases": [
            "Hippocampal body"
        ],
        "functions": [
            "Processes spatial representations and episodic sequences.",
            "Consolidates declarative memories through replay events."
        ],
        "connections": [
            "Receives entorhinal perforant path input and septal cholinergic modulation.",
            "Projects to subiculum, fornix, and anterior thalamic nuclei."
        ]
    },
    "107": {
        "description": "Posterior hippocampal segment emphasizing spatial memory and navigation precision.",
        "aliases": [
            "Hippocampal tail"
        ],
        "functions": [
            "Encodes fine-grained spatial maps and boundary representations.",
            "Supports contextual discrimination and scene memory."
        ],
        "connections": [
            "Receives input from parahippocampal cortex and retrosplenial areas.",
            "Projects to posterior cingulate cortex and thalamic nuclei."
        ]
    },
    "108": {
        "description": "Posterior long gyri of the insula processing somatosensory and vestibular signals.",
        "aliases": [
            "Posterior insular gyri"
        ],
        "functions": [
            "Integrate visceral pain, thermosensory, and vestibular information.",
            "Contribute to body awareness and sensorimotor integration."
        ],
        "connections": [
            "Receive input from thalamic ventromedial posterior nucleus and vestibular nuclei.",
            "Project to parietal operculum, cingulate cortex, and amygdala."
        ]
    },
    "109": {
        "description": "Anterior short gyri of the insula involved in gustation, interoception, and emotion.",
        "aliases": [
            "Anterior insular gyri"
        ],
        "functions": [
            "Process taste, visceral sensation, and autonomic states.",
            "Support empathy, subjective feeling, and risk evaluation."
        ],
        "connections": [
            "Receive gustatory input via thalamic VPMpc and limbic afferents.",
            "Project to orbitofrontal cortex, anterior cingulate, and amygdala."
        ]
    },
    "110": {
        "description": "Transition zone at the junction of insular cortex and frontal operculum.",
        "aliases": [
            "Limen insulae"
        ],
        "functions": [
            "Mediates integration of olfactory and gustatory signals entering the insula.",
            "Supports switching between limbic and neocortical processing streams."
        ],
        "connections": [
            "Receives fibers from olfactory tract and orbitofrontal cortex.",
            "Connects with anterior insula, amygdala, and frontal opercular regions."
        ]
    },
    "111": {
        "description": "Midbrain pretectal region coordinating pupillary light reflexes and visual attention.",
        "aliases": [
            "Pretectum"
        ],
        "functions": [
            "Controls consensual pupillary constriction via olivary pretectal nucleus.",
            "Integrates visual motion cues for reflexive eye movements."
        ],
        "connections": [
            "Receives retinal ganglion cell input through the brachium of the superior colliculus.",
            "Projects to Edinger–Westphal nucleus and superior colliculus."
        ]
    },
    "112": {
        "description": "Central midbrain tegmental territory containing ascending arousal and motor pathways.",
        "aliases": [
            "Midbrain tegmentum"
        ],
        "functions": [
            "Maintains arousal and reward processing via dopaminergic and cholinergic nuclei.",
            "Integrates cerebellar and basal ganglia signals for motor coordination."
        ],
        "connections": [
            "Receives input from cerebellar nuclei, basal ganglia, and limbic structures.",
            "Projects to thalamus, spinal cord, and cortex through ascending reticular pathways."
        ]
    },
    "113": {
        "description": "Ovoid midbrain nucleus conveying cerebellar output to motor cortex.",
        "aliases": [
            "Nucleus ruber",
            "Red nucleus"
        ],
        "functions": [
            "Facilitates limb flexor control and motor learning through rubrospinal pathways.",
            "Participates in error correction for voluntary movement."
        ],
        "connections": [
            "Receives input from deep cerebellar nuclei and motor cortex.",
            "Projects via rubrospinal tract and to inferior olive through central tegmental tract."
        ]
    },
    "114": {
        "description": "Basal midbrain nucleus containing dopaminergic cells regulating movement and reward.",
        "aliases": [
            "Substantia nigra pars compacta and pars reticulata",
            "SN"
        ],
        "functions": [
            "Pars compacta supplies dopamine to the striatum for motor learning and reinforcement.",
            "Pars reticulata provides inhibitory output influencing eye and limb movements."
        ],
        "connections": [
            "Receives afferents from striatum, subthalamic nucleus, and cortex.",
            "Projects to thalamus, superior colliculus, and striatum via dopaminergic pathways."
        ]
    },
    "115": {
        "description": "Dorsal midbrain structure orchestrating orienting movements and visual attention.",
        "aliases": [
            "Superior tectal colliculus"
        ],
        "functions": [
            "Integrates visual, auditory, and somatosensory stimuli to guide eye and head movements.",
            "Generates saccades and attentional shifts to salient targets."
        ],
        "connections": [
            "Receives retinal input and cortical projections from frontal eye fields and parietal cortex.",
            "Projects to brainstem gaze centers and spinal cord via tectospinal pathways."
        ]
    },
    "116": {
        "description": "Paired midbrain auditory centers processing sound localization and reflexes.",
        "aliases": [
            "Inferior tectal colliculus"
        ],
        "functions": [
            "Integrates binaural auditory cues for spatial localization.",
            "Drives auditory startle and orienting responses."
        ],
        "connections": [
            "Receives input from cochlear nuclei and superior olive via the lateral lemniscus.",
            "Projects to medial geniculate nucleus and auditory brainstem nuclei."
        ]
    },
    "117": {
        "description": "Massive fiber bundles on ventral midbrain conveying corticospinal, corticobulbar, and corticopontine tracts.",
        "aliases": [
            "Crus cerebri",
            "Cerebral peduncle"
        ],
        "functions": [
            "Transmit cortical motor commands to brainstem and spinal cord.",
            "Carry corticopontine fibers linking cortex to cerebellum for motor planning."
        ],
        "connections": [
            "Receive descending fibers from frontal, parietal, temporal, and occipital cortex.",
            "Project to pontine nuclei, cranial nerve motor nuclei, and spinal cord."
        ]
    },
    "118": {
        "description": "Major efferent pathway conveying cerebellar output to midbrain and thalamus.",
        "aliases": [
            "Brachium conjunctivum",
            "Superior cerebellar peduncle"
        ],
        "functions": [
            "Transmits dentate and interposed nuclei signals for motor coordination.",
            "Mediates cerebellar influence on eye movements and posture."
        ],
        "connections": [
            "Originates from deep cerebellar nuclei.",
            "Decussates in the midbrain and projects to red nucleus and thalamus."
        ]
    },
    "119": {
        "description": "Narrow channel linking third and fourth ventricles through the midbrain.",
        "aliases": [
            "Aqueduct of Sylvius",
            "Cerebral aqueduct"
        ],
        "functions": [
            "Conducts cerebrospinal fluid from the third to the fourth ventricle.",
            "Contains periaqueductal gray that modulates pain and defensive behavior."
        ],
        "connections": [
            "Receives CSF inflow from third ventricle.",
            "Drains into fourth ventricle and is surrounded by periaqueductal gray projections."
        ]
    },
    "120": {
        "description": "Intermediate cerebellar zone flanking the vermis to coordinate limb movements.",
        "aliases": [
            "Cerebellar paravermis",
            "Intermediate cerebellum"
        ],
        "functions": [
            "Refines ongoing limb movements via spinocerebellar inputs.",
            "Participates in motor learning and error correction."
        ],
        "connections": [
            "Receives proprioceptive input through spinocerebellar tracts and cortical pontine fibers.",
            "Projects via interposed nuclei to red nucleus and thalamic motor areas."
        ]
    },
    "121": {
        "description": "Lateral cerebellar hemispheres mediating motor planning and cognitive timing.",
        "aliases": [
            "Cerebrocerebellum"
        ],
        "functions": [
            "Supports planning of skilled movements and motor sequencing.",
            "Contributes to language, working memory, and executive functions."
        ],
        "connections": [
            "Receive corticopontine input from association cortices.",
            "Project via dentate nucleus to ventrolateral thalamus and prefrontal cortex."
        ]
    },
    "122": {
        "description": "Ventral pons containing corticospinal fibers and pontine nuclei.",
        "aliases": [
            "Basilar pons"
        ],
        "functions": [
            "Relays cortical motor plans to cerebellum via pontocerebellar pathways.",
            "Contains descending tracts controlling voluntary movement."
        ],
        "connections": [
            "Receives corticopontine fibers from frontal, parietal, and temporal cortex.",
            "Projects mossy fibers to cerebellar hemispheres through middle cerebellar peduncle."
        ]
    },
    "123": {
        "description": "Dorsal pontine tegmentum with cranial nerve nuclei and reticular formation.",
        "aliases": [
            "Pontine tegmentum"
        ],
        "functions": [
            "Regulates sleep-wake cycles, respiration, and eye movements.",
            "Integrates sensory information for reflexive motor responses."
        ],
        "connections": [
            "Receives input from vestibular system, cerebellum, and spinal cord.",
            "Projects to thalamus, cerebellum, and medullary reticular nuclei."
        ]
    },
    "124": {
        "description": "Anterior medulla containing corticospinal pyramids for voluntary motor control.",
        "aliases": [
            "Medullary pyramids"
        ],
        "functions": [
            "Transmit corticospinal commands to spinal motor neurons.",
            "Provide pathway for skilled voluntary movements."
        ],
        "connections": [
            "Receive descending fibers from motor and premotor cortex.",
            "Continue as lateral corticospinal tract after pyramidal decussation."
        ]
    },
    "125": {
        "description": "Dorsal medullary tegmentum housing cranial nerve nuclei and reticular circuits.",
        "aliases": [
            "Medullary tegmentum"
        ],
        "functions": [
            "Coordinates autonomic functions including respiration and cardiovascular control.",
            "Contains relay nuclei for sensory integration and motor reflexes."
        ],
        "connections": [
            "Receives input from spinal cord, cerebellum, and higher brain centers.",
            "Projects to thalamus, cerebellum, and spinal cord via ascending and descending tracts."
        ]
    },
    "126": {
        "description": "Medullary nucleus that computes timing signals for cerebellar learning.",
        "aliases": [
            "Inferior olivary complex"
        ],
        "functions": [
            "Provides climbing fiber input to cerebellar Purkinje cells for motor learning.",
            "Synchronizes cerebellar oscillations important for coordination."
        ],
        "connections": [
            "Receives projections from red nucleus, spinal cord, and cortex.",
            "Projects climbing fibers through inferior cerebellar peduncle to cerebellar cortex."
        ]
    },
    "127": {
        "description": "Large fiber bundle conveying spinal and medullary inputs to cerebellum.",
        "aliases": [
            "Restiform body",
            "Inferior cerebellar peduncle"
        ],
        "functions": [
            "Transmits proprioceptive and vestibular information to cerebellar cortex.",
            "Carries efferent fibers from cerebellum to vestibular nuclei."
        ],
        "connections": [
            "Receives dorsal spinocerebellar, cuneocerebellar, and olivocerebellar fibers.",
            "Projects to vestibular nuclei and deep cerebellar nuclei."
        ]
    },
    "128": {
        "description": "Massive pontocerebellar fiber tract linking cerebral cortex with cerebellum.",
        "aliases": [
            "Brachium pontis",
            "Middle cerebellar peduncle"
        ],
        "functions": [
            "Conveys pontine mossy fibers that carry cortical planning information.",
            "Coordinates bilateral cerebellar processing for skilled movement."
        ],
        "connections": [
            "Receives pontine nuclei axons derived from corticopontine tracts.",
            "Projects to cerebellar hemispheres distributing mossy fiber input."
        ]
    },
    "129": {
        "description": "Diamond-shaped cavity between brainstem and cerebellum containing cerebrospinal fluid.",
        "aliases": [
            "Fourth cerebral ventricle"
        ],
        "functions": [
            "Distributes CSF to subarachnoid space via median and lateral apertures.",
            "Provides ventricular surface for nuclei regulating autonomic and vestibular function."
        ],
        "connections": [
            "Receives CSF from cerebral aqueduct and spinal central canal.",
            "Communicates with subarachnoid space through foramen of Magendie and Luschka."
        ]
    },
    "130": {
        "description": "Continuation of the ventricular system within the medulla and spinal cord.",
        "aliases": [
            "Central canal"
        ],
        "functions": [
            "Conducts cerebrospinal fluid along the spinal axis.",
            "Serves as pathway for neural stem cells and ependymal signaling."
        ],
        "connections": [
            "Receives CSF from the fourth ventricle.",
            "Extends caudally through spinal cord and connects rostrally to obex region."
        ]
    },
    "131": {
        "description": "Midline thalamic nuclei cluster coordinating arousal and limbic integration.",
        "aliases": [
            "Midline nuclear complex"
        ],
        "functions": [
            "Supports memory consolidation, attention, and emotional regulation.",
            "Provides diffuse thalamocortical modulation of cortical excitability."
        ],
        "connections": [
            "Receives input from hypothalamus, hippocampus, and brainstem reticular formation.",
            "Projects to prefrontal cortex, cingulate gyrus, and nucleus accumbens."
        ]
    },
    "132": {
        "description": "Lateral olfactory gyrus relaying smell information to orbitofrontal and temporal regions.",
        "aliases": [
            "Lateral olfactory area"
        ],
        "functions": [
            "Supports conscious odor discrimination and associative learning.",
            "Integrates olfactory inputs with reward and memory systems."
        ],
        "connections": [
            "Receives projections from olfactory bulb via lateral olfactory tract.",
            "Projects to piriform cortex, orbitofrontal cortex, and amygdala."
        ]
    },
    "133": {
        "description": "Parietal operculum covering the insula and processing somatosensory and gustatory stimuli.",
        "aliases": [
            "Secondary somatosensory cortex",
            "SII"
        ],
        "functions": [
            "Encodes texture, pain, and tactile discrimination for bilateral body regions.",
            "Integrates taste and visceral sensations with sensorimotor planning."
        ],
        "connections": [
            "Receives thalamic input from ventral posterior inferior nucleus and insular cortex.",
            "Projects to insula, cingulate cortex, and premotor areas."
        ]
    },
    "134": {
        "description": "Inferior putamen subdivision heavily engaged in sensorimotor basal ganglia circuits.",
        "aliases": [
            "Posteroventral putamen"
        ],
        "functions": [
            "Modulates habitual motor responses and movement vigor.",
            "Integrates somatosensory feedback with motor plans."
        ],
        "connections": [
            "Receives dense corticostriatal projections from primary motor and somatosensory cortices.",
            "Projects to globus pallidus externus and substantia nigra pars reticulata."
        ]
    },
    "135": {
        "description": "Medial frontal gyrus adjacent to cingulate sulcus involved in cognitive control and empathy.",
        "aliases": [
            "Paracingulate sulcus gyrus"
        ],
        "functions": [
            "Monitors action selection and social decision making.",
            "Supports mentalizing and conflict resolution tasks."
        ],
        "connections": [
            "Receives input from anterior cingulate, dorsolateral prefrontal, and temporal poles.",
            "Projects to medial prefrontal cortex, premotor areas, and striatum."
        ]
    },
    "136": {
        "description": "Frontal gyrus along the superior frontal sulcus contributing to working memory and eye movement control.",
        "aliases": [
            "Rostral middle frontal gyrus"
        ],
        "functions": [
            "Maintains task rules and goals during complex behaviors.",
            "Coordinates saccadic planning with dorsolateral prefrontal networks."
        ],
        "connections": [
            "Receives inputs from parietal cortex, frontal eye fields, and anterior cingulate.",
            "Projects to caudate nucleus, premotor cortex, and mediodorsal thalamus."
        ]
    },
    "137": {
        "description": "Anterior-most frontal gyrus bordering the orbital surface and participating in socioemotional cognition.",
        "aliases": [
            "Frontomarginal gyrus of Wernicke"
        ],
        "functions": [
            "Evaluates complex social cues and integrates reward expectations.",
            "Contributes to decision making under uncertainty."
        ],
        "connections": [
            "Receives input from temporal pole, amygdala, and medial prefrontal cortex.",
            "Projects to orbitofrontal cortex, ventral striatum, and anterior cingulate."
        ]
    },
    "138": {
        "description": "Tip of the frontal lobe engaged in abstract reasoning, future planning, and social cognition.",
        "aliases": [
            "Frontal pole",
            "Brodmann area 10"
        ],
        "functions": [
            "Supports prospective memory, multitasking, and metacognition.",
            "Integrates affective and cognitive information for strategic planning."
        ],
        "connections": [
            "Receives afferents from temporal pole, parietal cortex, and limbic structures.",
            "Projects to dorsolateral prefrontal cortex, medial prefrontal regions, and caudate nucleus."
        ]
    },
    "139": {
        "description": "Medial temporal cortical area integrating object recognition with contextual memory.",
        "aliases": [
            "Perirhinal cortex",
            "Brodmann areas 35/36"
        ],
        "functions": [
            "Supports familiarity-based recognition memory and associative learning.",
            "Links sensory features with hippocampal episodic representations."
        ],
        "connections": [
            "Receives input from ventral visual stream and olfactory cortex.",
            "Projects to entorhinal cortex, hippocampus, and orbitofrontal areas."
        ]
    },
    "140": {
        "description": "Fan-shaped projection fibers carrying visual information from thalamus to occipital cortex.",
        "aliases": [
            "Geniculocalcarine tract",
            "Optic radiation"
        ],
        "functions": [
            "Transmits retinotopic visual data essential for conscious perception.",
            "Segments into Meyer’s loop and dorsal bundle to relay upper and lower visual field information."
        ],
        "connections": [
            "Originate from lateral geniculate nucleus neurons.",
            "Project to primary visual cortex along the calcarine fissure with collateral branches to extrastriate areas."
        ]
    },
    "141": {
        "description": "Expanded junction of the lateral ventricle connecting its body with temporal and occipital horns.",
        "aliases": [
            "Trigone of lateral ventricle"
        ],
        "functions": [
            "Channels cerebrospinal fluid between ventricular horns.",
            "Serves as anatomical landmark for choroid plexus and white matter tracts."
        ],
        "connections": [
            "Continuous with body, posterior horn, and inferior horn of the lateral ventricle.",
            "Borders the tapetum, splenium of corpus callosum, and hippocampal tail."
        ]
    }
}

def main():
    path = Path('public/reference.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    for key, fields in updates.items():
        if key not in data:
            raise KeyError(f"Missing id {key}")
        data[key].update(fields)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding='utf-8')

if __name__ == '__main__':
    main()
