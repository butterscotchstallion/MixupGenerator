<script lang="ts">
	import { Icon, type IconType } from 'svelte-icons-pack';
	import { AiOutlineCheckSquare, AiOutlineCloseSquare } from 'svelte-icons-pack/ai';
	import { BiError } from 'svelte-icons-pack/bi';

	export let title: string;
	export let message: string;
	export let type: string = 'success';

	let icon: IconType = AiOutlineCheckSquare;
	let alertType = 'variant-filled-success';
	if (type === 'error') {
		icon = BiError;
		alertType = 'variant-filled-error';
	}
</script>

<aside class="alert {alertType} mb-2">
	<div>
		<Icon
			className="icons"
			size="32"
			src={icon}
		/>
	</div>
	<div class="alert-message">
		<h3 class="h3">{title}</h3>
		<p>{message}</p>
	</div>

	<div class="close-button">
		<Icon
			className="icons"
			size="32"
			src={AiOutlineCloseSquare}
		/>
	</div>
</aside>

<style lang="scss">
	.close-button {
		position: absolute;
		top: 3px;
		right: 3px;
	}
</style>
