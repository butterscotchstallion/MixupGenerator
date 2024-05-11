<script lang="ts">
	import type { ITeam } from '$lib/i-team';
	import { Icon } from 'svelte-icons-pack';
	import { BiError } from 'svelte-icons-pack/bi';
	import { RiUserFacesTeamLine } from 'svelte-icons-pack/ri';
	import TeamMemberLink from './TeamMemberLink.svelte';

	export let teams: ITeam[];
	export let teamsResponseError: TypeError;
	export let loading: boolean;
</script>

{#if teamsResponseError}
	<aside class="alert variant-ghost">
		<!-- Icon -->
		<div>
			<Icon
				className="icons"
				size="32"
				src={BiError}
			/>
		</div>
		<!-- Message -->
		<div class="alert-message">
			<h3 class="h3">API Error</h3>
			<p>There was a problem connecting to the API: <code>{teamsResponseError}</code></p>
		</div>
	</aside>
{:else}
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

<style>
	.team-members-count {
		padding-left: 0.25rem;
	}
</style>
