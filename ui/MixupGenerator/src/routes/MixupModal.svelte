<script lang="ts">
	export let showModal: boolean;

	let dialog: HTMLDialogElement;

	$: if (dialog && showModal) dialog.showModal();
</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
<dialog
	bind:this={dialog}
	on:close={() => (showModal = false)}
	on:click|self={() => dialog.close()}
>
	<div class="mixup-modal">
		<!-- svelte-ignore a11y-no-static-element-interactions -->
		<div on:click|stopPropagation>
			<header>
				<h4 class="h4"><slot name="header" /></h4>
				<hr class="hr" />
			</header>

			<section class="mt-2 mb-2">
				<slot name="body" />
			</section>

			<footer class="modal-footer">
				<div class="button-wrapper">
					<button
						class="btn btn-sm variant-ghost-surface"
						on:click={() => {
							dialog.close();
						}}>Cancel</button
					>
					<slot name="footer" />
				</div>
			</footer>
		</div>
	</div>
</dialog>

<style lang="scss">
	.button-wrapper {
		display: flex;
		justify-content: right;

		button {
			margin-right: 1rem;
			&:last-child {
				margin: 0;
			}
		}
	}

	dialog {
		max-width: 32em;
		min-width: 30vw;
		border-radius: 0.2em;
		border: none;
		padding: 0;
		background: rgba(var(--color-surface-900) / 1);
		color: var(--text-primary-500);
		border: 1px solid rgba(var(--color-surface-500) / 1);
	}
	dialog::backdrop {
		background: rgba(0, 0, 0, 0.75);
	}
	dialog > div {
		padding: 1em;
	}
	dialog[open] {
		animation: zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
	}
	@keyframes zoom {
		from {
			transform: scale(0.95);
		}
		to {
			transform: scale(1);
		}
	}
	dialog[open]::backdrop {
		animation: fade 0.2s ease-out;
	}
	@keyframes fade {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
</style>
