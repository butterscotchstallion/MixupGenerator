<script>
	let teams$ = getTeams();

	async function getTeams() {
		const res = await fetch('http://127.0.0.1:8000/api/teams');
		const responseJSON = await res.text();

		if (res.ok) {
			return JSON.parse(responseJSON).teams;
		} else {
			throw new Error(responseJSON);
		}
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
