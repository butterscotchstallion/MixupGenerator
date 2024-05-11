<script lang="ts">
	import '../app.postcss';

	import { initializeStores, Modal } from '@skeletonlabs/skeleton';
	initializeStores();

	// Floating UI for Popups
	import { arrow, autoUpdate, computePosition, flip, offset, shift } from '@floating-ui/dom';
	import { storePopup, type ModalComponent } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	import { default as MixupModal } from './MixupModal.svelte';

	const modalRegistry: Record<string, ModalComponent> = {
		// Set a unique modal ID, then pass the component reference
		modalComponentOne: { ref: MixupModal },
	};
</script>

<Modal components={modalRegistry} />

<slot />
