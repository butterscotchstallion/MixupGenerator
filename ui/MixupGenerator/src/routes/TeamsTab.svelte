<script lang="ts">
	import api from '$lib/api';
	import type { ITeam } from '$lib/i-team';
	import type { AxiosError, AxiosResponse } from 'axios';
	import { Icon } from 'svelte-icons-pack';
	import { AiOutlineUsergroupAdd } from 'svelte-icons-pack/ai';
	import { RiUserFacesTeamLine } from 'svelte-icons-pack/ri';
	import AlertBox from './AlertBox.svelte';
	import MixupModal from './MixupModal.svelte';
	import TeamMemberLink from './TeamMemberLink.svelte';

	export let teams: ITeam[];
	export let teamsResponseError: TypeError;
	export let loading: boolean;

	let addTeamError: string = '';
	let addTeamSuccess = false;
	let isAddingTeam = false;
	$: showModal = false;

	let teamFormData = {
		name: '',
	};

	function toggleModal() {
		showModal = !showModal;
	}

	function clearMessages() {
		addTeamError = '';
		addTeamSuccess = false;
		isAddingTeam = false;
		teamFormData = {
			name: '',
		};
	}

	function onFormSubmit() {
		api.addTeam$(teamFormData.name).then(
			(response: AxiosResponse) => {
				addTeamSuccess = true;
				toggleModal();
			},
			(error: AxiosError) => {
				addTeamError = error.message;
			},
		);
	}
</script>

{#if teamsResponseError}
	<AlertBox
		title="API Error"
		message="There was a problem connecting to the API: <code>{teamsResponseError}</code>"
	/>
{:else}
	{#if addTeamSuccess}
		<section class="mb-2">
			<AlertBox
				title="Success"
				message="New team added successfully!"
			></AlertBox>
		</section>
	{/if}

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
			<span>Add Team</span>
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
		{#if addTeamError}
			<AlertBox
				type="error"
				title="Error adding team"
				message="There was a problem adding the team: {addTeamError}"
			/>
		{/if}
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
			disabled={isAddingTeam || teamFormData.name.trim().length === 0}
			class="btn btn-sm variant-filled"
			on:click={onFormSubmit}
		>
			<Icon
				className="icons"
				src={AiOutlineUsergroupAdd}
			/>
			{isAddingTeam ? 'Adding team...' : 'Add Team'}
		</button>
	</div>
</MixupModal>

<style>
	.team-members-count {
		padding-left: 0.25rem;
	}
</style>
