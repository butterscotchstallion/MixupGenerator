<script lang="ts">
	import type { ITeam } from '$lib/i-team';
	import type { ITeamMember } from '$lib/i-team-member';
	import type { ITeamMemberLinkResponse } from '$lib/i-team-member-link-response';
	import type { ITeamResponse } from '$lib/i-team-response';
	import { Tab, TabGroup } from '@skeletonlabs/skeleton';
	import { BehaviorSubject, Subscription, forkJoin } from 'rxjs';
	import { onDestroy, onMount } from 'svelte';
	import { Icon } from 'svelte-icons-pack';
	import { BsCalendarDay } from 'svelte-icons-pack/bs';
	import { RiUserFacesTeamLine } from 'svelte-icons-pack/ri';
	import MeetingsTab from './MeetingsTab.svelte';
	import TeamMemberLink from './TeamMemberLink.svelte';

	const teams$ = new BehaviorSubject<ITeam[]>([]);
	const subscriptions = new Subscription();
	const teamMemberIdToTeamsMap: Map<number, ITeam[]> = new Map<number, ITeam[]>();
	let tabSet: number = 0;

	async function parseTeamsData() {
		subscriptions.add(
			getTeamsData$().subscribe(async (responses) => {
				const teams: ITeam[] = [];
				const teamMembersResponse: ITeamMember[] = JSON.parse(
					await responses[2].text(),
				).team_members;
				const teamsResponse: ITeamResponse[] = JSON.parse(await responses[0].text()).teams;
				const teamMembersLinksResponse: ITeamMemberLinkResponse[] = JSON.parse(
					await responses[1].text(),
				).team_member_team_link;
				const teamIdToTeamMembersMap: Map<number, ITeamMember[]> = new Map<number, ITeamMember[]>();
				const teamMemberIdToTeamMembersMap: Map<number, ITeamMember> = new Map<
					number,
					ITeamMember
				>();
				const teamIdToTeamsMap: Map<number, ITeam> = new Map<number, ITeam>();
				const teamMemberIdToTeamIdsMap: Map<number, number[]> = new Map<number, number[]>();

				teamMembersResponse?.forEach((teamMember: ITeamMember) => {
					teamMemberIdToTeamMembersMap.set(teamMember.id, teamMember);
				});

				/**
				 * 1. Iterate team members links and build a map of
				 * team -> team members
				 * 2. Since team members can be on multiple teams, we have
				 * to account for the scenario of seeing the same team again
				 * and merge the members
				 * 3. The value for the map is a list of team members
				 *
				 */
				teamMembersLinksResponse.forEach((teamMembers: ITeamMemberLinkResponse) => {
					const existingTeamMembers = teamIdToTeamMembersMap.get(teamMembers.team_id);
					const existingTeamIds = teamMemberIdToTeamIdsMap.get(teamMembers.team_member_id);
					const teamMember = teamMemberIdToTeamMembersMap.get(teamMembers.team_member_id);
					let teamMemberTeamIds: number[] = [teamMembers.team_id];

					// Handle team member id -> teams
					if (existingTeamIds) {
						teamMemberTeamIds = [...teamMemberTeamIds, teamMembers.team_id];
					}

					teamMemberIdToTeamIdsMap.set(teamMembers.team_member_id, teamMemberTeamIds);

					// Handle team id -> team members
					if (teamMember) {
						let members: ITeamMember[] = [teamMember];

						if (existingTeamMembers) {
							members = [...existingTeamMembers, teamMember];
						}

						teamIdToTeamMembersMap.set(teamMembers.team_id, members);
					}
				});

				teamsResponse.forEach((team: ITeam) => {
					let members: ITeamMember[] = teamIdToTeamMembersMap.get(team.id) || [];
					members.sort((a: ITeamMember, b: ITeamMember) => a.name.localeCompare(b.name));
					members = members.map((member: ITeamMember) => {
						// This isn't working because the map is defined below
						const teams = teamMemberIdToTeamsMap.get(member.id) || [];
						const teamNames = teams.map((t: ITeam) => t.name);
						member.teams = teams;
						member.teamNames = teamNames.join(', ');
						return member;
					});

					team.members = members;
					teams.push(team);

					teamIdToTeamsMap.set(team.id, team);
				});

				teamMemberIdToTeamIdsMap.forEach((teamIds: number[], teamMemberId: number) => {
					const teams: ITeam[] = [];
					teamIds.forEach((index: number, teamId: number) => {
						const team: ITeam | undefined = teamIdToTeamsMap.get(teamId);
						if (team) {
							teams.push(team);
						}
					});
					teamMemberIdToTeamsMap.set(teamMemberId, teams);
				});

				teams.sort((a: ITeam, b: ITeam) => a.name.localeCompare(b.name));

				teams$.next(teams);
			}),
		);
	}

	function getTeamsData$() {
		return forkJoin([
			fetch('http://127.0.0.1:8000/api/teams'),
			fetch('http://127.0.0.1:8000/api/team-member-team-link'),
			fetch('http://127.0.0.1:8000/api/team-members'),
		]);
	}

	onDestroy(() => {
		subscriptions.unsubscribe();
	});

	onMount(() => {
		parseTeamsData();
	});
</script>

<div class="container h-full mx-auto flex justify-center">
	<div class="grid grid-flow-row auto-rows-max">
		<h1 class="h1 m-1">
			<span
				class="bg-gradient-to-br from-red-500 to-yellow-500 bg-clip-text text-transparent box-decoration-clone"
			>
				Mixup Generator
			</span>
		</h1>

		<TabGroup>
			<Tab
				bind:group={tabSet}
				name="tab1"
				value={0}
			>
				<span>
					<Icon
						className="icons"
						src={RiUserFacesTeamLine}
					/>
					Teams
				</span>
			</Tab>
			<Tab
				bind:group={tabSet}
				name="tab2"
				value={1}
			>
				<Icon
					className="icons"
					src={BsCalendarDay}
				/>
				Meetings
			</Tab>
			<!-- Tab Panels --->
			<svelte:fragment slot="panel">
				{#if tabSet === 0}
					<div class="table-container">
						<table class="table table-hover">
							<thead>
								<tr>
									<th>Teams</th>
									<th>Members</th>
								</tr>
							</thead>
							<tbody>
								{#if teams$ === null}
									<tr><td colspan="2"><div class="placeholder" /></td></tr>
									<tr><td colspan="2"><div class="placeholder" /></td></tr>
									<tr><td colspan="2"><div class="placeholder" /></td></tr>
									<tr><td colspan="2"><div class="placeholder" /></td></tr>
								{:else}
									{#each $teams$ as team}
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
				{:else if tabSet === 1}
					<MeetingsTab />
				{/if}
			</svelte:fragment>
		</TabGroup>
	</div>
</div>

<style>
	:global(.icons) {
		display: inline;
	}

	.team-members-count {
		padding-left: 0.25rem;
	}
</style>
