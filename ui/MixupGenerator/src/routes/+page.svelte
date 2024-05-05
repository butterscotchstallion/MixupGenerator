<script lang="ts">
	import type { ITeam } from '$lib/i-team';
	import type { ITeamMember } from '$lib/i-team-member';
	import type { ITeamMemberLinkResponse } from '$lib/i-team-member-link-response';
	import type { ITeamResponse } from '$lib/i-team-response';
	import { BehaviorSubject, forkJoin } from 'rxjs';

	const teams$ = new BehaviorSubject<ITeam[]>([]);

	async function parseTeamsData() {
		getTeamsData$().subscribe(async (responses) => {
			const teams: ITeam[] = [];
			const teamMembersResponse: ITeamMember[] = JSON.parse(await responses[2].text()).team_members;
			const teamsResponse: ITeamResponse[] = JSON.parse(await responses[0].text()).teams;
			const teamMembersLinksResponse: ITeamMemberLinkResponse[] = JSON.parse(
				await responses[1].text()
			).team_member_team_link;
			//const teamsMap: Map<number, ITeam> = new Map<number, ITeam>();
			// team_id -> ITeamMember[]
			const teamToTeamMembersMap: Map<number, ITeamMember[]> = new Map<number, ITeamMember[]>();
			const teamMemberIdToTeamMemberMap: Map<number, ITeamMember> = new Map<number, ITeamMember>();

			teamMembersResponse.forEach((teamMember: ITeamMember) => {
				teamMemberIdToTeamMemberMap.set(teamMember.id, teamMember);
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
				const existingTeamMembers = teamToTeamMembersMap.get(teamMembers.team_id);
				const teamMember = teamMemberIdToTeamMemberMap.get(teamMembers.team_member_id);

				if (teamMember) {
					let members: ITeamMember[] = [teamMember];

					if (existingTeamMembers) {
						members = [...existingTeamMembers, teamMember];
					}

					teamToTeamMembersMap.set(teamMembers.team_id, members);
				}
			});

			teamsResponse.forEach((team: ITeam) => {
				const members: ITeamMember[] = teamToTeamMembersMap.get(team.id) || [];
				team.members = members;
				teams.push(team);
			});

			teams$.next(teams);
		});
	}

	function getTeamsData$() {
		return forkJoin([
			fetch('http://127.0.0.1:8000/api/teams'),
			fetch('http://127.0.0.1:8000/api/team-member-team-link'),
			fetch('http://127.0.0.1:8000/api/team-members')
		]);
	}
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="grid grid-cols-1 gap-4">
		<header class="card-header">
			<h1 class="h1">
				<span
					class="bg-gradient-to-br from-red-500 to-yellow-500 bg-clip-text text-transparent box-decoration-clone"
				>
					Mixup Generator
				</span>
			</h1>
		</header>

		<section class="p-4">
			<div class="table-container">
				<!-- Native Table Element -->
				<table class="table table-hover">
					<thead>
						<tr>
							<th>Teams</th>
						</tr>
					</thead>
					<tbody>
						{#await teams$}
							<tr><td colspan="2"><div class="placeholder" /></td></tr>
							<tr><td colspan="2"><div class="placeholder" /></td></tr>
							<tr><td colspan="2"><div class="placeholder" /></td></tr>
							<tr><td colspan="2"><div class="placeholder" /></td></tr>
						{:then teams}
							{#each teams as team}
								<tr>
									<td>{team.name}</td>
								</tr>
							{/each}
						{:catch error}
							<tr><td colspan="2"><p style="color: red">Error: it didn't work</p></td></tr>
						{/await}
					</tbody>
				</table>
			</div>
		</section>
	</div>
</div>
