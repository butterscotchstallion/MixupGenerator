<script lang="ts">
	import type { ITeam } from '$lib/i-team';
	import { Icon } from 'svelte-icons-pack';
	import { AiOutlineUsergroupAdd } from 'svelte-icons-pack/ai';
	import { BiError } from 'svelte-icons-pack/bi';
	import { RiUserFacesTeamLine } from 'svelte-icons-pack/ri';
	import MixupModal from './MixupModal.svelte';
	import TeamMemberLink from './TeamMemberLink.svelte';

	export let teams: ITeam[];
	export let teamsResponseError: TypeError;
	export let loading: boolean;

	$: showModal = false;

	const teamFormData = {
		name: '',
	};

	function toggleModal() {
		showModal = !showModal;
	}

	function onFormSubmit() {
		alert(teamFormData);
	}
</script>

{#if teamsResponseError}
	<aside class="alert variant-ghost">
		<div>
			<Icon
				className="icons"
				size="32"
				src={BiError}
			/>
		</div>
		<div class="alert-message">
			<h3 class="h3">API Error</h3>
			<p>There was a problem connecting to the API: <code>{teamsResponseError}</code></p>
		</div>
	</aside>
{:else}
	<section class="mb-2">
		<button
			type="button"
			class="btn btn-sm variant-filled"
			on:click={() => toggleModal()}
		>
			<span
				><Icon
					className="icons"
					src={AiOutlineUsergroupAdd}
				/></span
			>
			<span>Edit Teams</span>
		</button>
	</section>
	<div class="table-container">
		<table class="table table-hover">
			<thead>
				<tr>
					<th>Teams</th>
					<th>Members</th>
				</tr>
			</thead>
			<tbody>
				{#if loading}
					<tr><td colspan="2"><div class="placeholder" /></td></tr>
					<tr><td colspan="2"><div class="placeholder" /></td></tr>
					<tr><td colspan="2"><div class="placeholder" /></td></tr>
					<tr><td colspan="2"><div class="placeholder" /></td></tr>
				{:else}
					{#each teams as team}
						<tr>
							<td>
								<span class="badge variant-filled-surface">
									<Icon
										className="icons"
										src={RiUserFacesTeamLine}
									/>&nbsp;
									{team.name}
								</span>
								{#if team?.members}
									<p class="team-members-count">
										<small>{team.members.length} members</small>
									</p>
								{/if}
							</td>
							<td>
								{#if team?.members && team.members.length > 0}
									<ul>
										{#each team?.members as member}
											<li class="p-1">
												<TeamMemberLink teamMember={member} />
											</li>
										{/each}
									</ul>
								{/if}
							</td>
						</tr>
					{/each}
				{/if}
			</tbody>
		</table>
	</div>
{/if}

<MixupModal bind:showModal>
	<h2 slot="header">Add Team</h2>
	<div slot="body">
		<form method="post">
			<label
				class="label"
				for="team-name"
			>
				<span>Team Name</span>
				<input
					class="input"
					type="text"
					maxlength="25"
					id="team-name"
					placeholder="Enter team name (25 characters max)"
					bind:value={teamFormData.name}
				/>
			</label>
		</form>
	</div>
	<div slot="footer">
		<button
			class="btn btn-sm variant-ghost-surface"
			on:click={() => {
				toggleModal();
			}}>Cancel</button
		>
		<button
			disabled={teamFormData.name.trim().length === 0}
			class="btn btn-sm variant-filled"
			on:click={onFormSubmit}>Add Team</button
		>
	</div>
</MixupModal>

<style>
	.team-members-count {
		padding-left: 0.25rem;
	}
</style>
