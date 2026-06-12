export default async function cleanupTriage({ github, context, core }) {
    const issueNumber = context.payload.issue?.number;

    if (!issueNumber) {
        core.info('No issue number found in context, skipping cleanup.');
        return;
    }

    const { data: issueData } = await github.rest.issues.get({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: issueNumber,
    });

    const labels = issueData.labels.map((l) =>
        typeof l === 'string' ? l : l.name,
    );

    // If both bot-triaged and need-triage exist, remove need-triage
    if (
        labels.includes('status/bot-triaged') &&
        labels.includes('status/need-triage')
    ) {
        await github.rest.issues.removeLabel({
            owner: context.repo.owner,
            repo: context.repo.repo,
            issue_number: issueNumber,
            name: 'status/need-triage',
        });
        core.info(`Removed status/need-triage from #${issueNumber}`);
    }

    // If both bot-triaged and manual-triage exist, remove bot-triaged
    if (
        labels.includes('status/bot-triaged') &&
        labels.includes('status/manual-triage')
    ) {
        await github.rest.issues.removeLabel({
            owner: context.repo.owner,
            repo: context.repo.repo,
            issue_number: issueNumber,
            name: 'status/bot-triaged',
        });
        core.info(
            `Removed status/bot-triaged from #${issueNumber} — requires manual triage`,
        );
    }

    core.info(`Label cleanup complete for #${issueNumber}`);
}
