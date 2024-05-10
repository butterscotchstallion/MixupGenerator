<script lang="ts">
	import type { ITeamMember } from '$lib/i-team-member';
	import { popup } from '@skeletonlabs/skeleton';
	import { Icon } from 'svelte-icons-pack';
	import { BsCalendar2Date, BsCalendarPlus, BsFilePerson, BsKey } from 'svelte-icons-pack/bs';
	import { RiUserFacesTeamLine } from 'svelte-icons-pack/ri';
	import Time from 'svelte-time';

	export let teamMember: ITeamMember;
</script>

{#if teamMember.can_attend_multiple_meetings}
	<Icon
		className="icons"
		src={BsCalendarPlus}
	/>
{/if}
<a
	class="anchor [&>*]:pointer-events-none"
	href="#modal"
	use:popup={{
		event: 'hover',
		target: 'popup-' + teamMember.id,
		placement: 'top',
	}}>{teamMember.name}</a
>

<div
	class="popup-card card p-2 variant-filled-tertiary"
	data-popup="popup-{teamMember.id}"
>
	<table>
		<tbody>
			<tr>
				<td>
					<Icon
						className="icons"
						src={BsFilePerson}
					/>
					Name
				</td>
				<td>{teamMember.name}</td>
			</tr>
			<tr>
				<td>
					<Icon
						className="icons"
						src={RiUserFacesTeamLine}
					/>
					Teams
				</td>
				<td>
					{#if teamMember?.teams && teamMember.teams.length > 0}
						{#each teamMember.teams as team}
							<p>{team.name}</p>
						{/each}
					{:else}
						None
					{/if}
				</td>
			</tr>
			<tr>
				<td>
					<Icon
						className="icons"
						src={BsCalendar2Date}
					/>
					Created
				</td>
				<td
					>Created <Time
						relative
						timestamp={teamMember.created_at}
					/></td
				>
			</tr>
			{#if teamMember.updated_at}
				<tr>
					<td>
						<Icon
							className="icons"
							src={BsCalendar2Date}
						/>
						Updated
					</td>
					<td>{teamMember.updated_at}</td>
				</tr>
			{/if}
			<tr>
				<td>
					<Icon
						className="icons"
						src={BsKey}
					/>
					KeyCloak ID
				</td>
				<td>{teamMember.keycloak_user_id}</td>
			</tr>
			{#if teamMember.can_attend_multiple_meetings}
				<tr>
					<td colspan="2">
						<Icon
							className="icons"
							src={BsCalendarPlus}
						/>
						Can attend multiple meetings
					</td>
				</tr>
			{/if}
		</tbody>
	</table>
	<div class="arrow variant-filled-tertiary" />
</div>

<style>
	.popup-card table tr {
		&:last-child {
			border-bottom: 0;
		}
	}
</style>
