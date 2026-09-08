"""Seeds the CaseTypeConfig/AgentPersona rows Dialex needs to run at all.

This is reference/admin config data, not schema — deliberately not a
migration (matches this project's existing no-migrations-for-config-data
convention, spec 0031). It's a management command instead of a one-off
shell session specifically so a dev DB wipe (or a fresh environment) can
restore it with one command rather than losing it silently again — this
exact gap already bit research_debate once before (spec 0030) and blocked
Phase 0's own verification (spec 0043) the second time.

Idempotent: safe to re-run, never duplicates or overwrites rows that
already exist.

The five personas' system_prompt text below is newly drafted (2026-09,
during spec 0043's Phase 0 verification) — the originals were created
directly via Django admin/shell at some point and were never committed
to any spec, so they were unrecoverable after the dev DB wipe. Only
loan_approval's "Credit Risk Officer"/"Relationship Loan Advisor"
personas and its required_fields/policy_context are restorations of
previously-documented content (spec 0031/0030) — everything else here
is new content, not a reconstruction of the original.
"""

from django.core.management.base import BaseCommand

from apps.dialex.cases.models import CaseTypeConfig
from apps.dialex.debates.models import AgentPersona

GPT4O_MINI = {"model": "gpt-4o-mini", "temperature": 0.7}


class Command(BaseCommand):
    help = "Seed the case-type configs and agent personas Dialex needs to run (idempotent)."

    def handle(self, *args, **options):
        moderator, _ = AgentPersona.objects.get_or_create(
            name="Moderator",
            role=AgentPersona.Role.JUDGE,
            defaults={
                "role_description": "Weighs each participant's arguments and delivers a final, reasoned verdict.",
                "system_prompt": (
                    "You are the Moderator, an impartial judge overseeing this debate. Weigh each "
                    "participant's arguments on the strength of their reasoning and evidence, not "
                    "eloquence alone. When guidance for this case type is provided, weigh convergence "
                    "against it explicitly. Stay procedural — you have no domain viewpoint of your own, "
                    "only the arguments in front of you and any case-type guidance given. Be clear and "
                    "direct in your verdict."
                ),
                "model_config": {"model": "gpt-4o-mini", "temperature": 0.3},
            },
        )

        pragmatist, _ = AgentPersona.objects.get_or_create(
            name="Pragmatist",
            role=AgentPersona.Role.PARTICIPANT,
            defaults={
                "role_description": "Argues from practical, cost- and time-conscious tradeoffs.",
                "system_prompt": (
                    "You are the Pragmatist. You argue from practical tradeoffs — cost, time-to-value, "
                    "and what's actually achievable given real constraints. You're skeptical of solutions "
                    "that sound good in theory but are expensive or slow to deliver. Be specific about the "
                    "tradeoff you see. Be brief — 2-3 sentences."
                ),
                "model_config": GPT4O_MINI,
            },
        )

        scale_minded, _ = AgentPersona.objects.get_or_create(
            name="Scale-minded",
            role=AgentPersona.Role.PARTICIPANT,
            defaults={
                "role_description": "Argues from long-term scalability and robustness.",
                "system_prompt": (
                    "You are Scale-minded. You argue from long-term scalability and robustness — what "
                    "will hold up as usage, data, or complexity grows, even if it costs more up front. "
                    "You're skeptical of shortcuts that work today but won't scale. Be specific about the "
                    "scaling concern you see. Be brief — 2-3 sentences."
                ),
                "model_config": GPT4O_MINI,
            },
        )

        credit_risk_officer, _ = AgentPersona.objects.get_or_create(
            name="Credit Risk Officer",
            role=AgentPersona.Role.PARTICIPANT,
            defaults={
                "role_description": "Weighs DTI, credit score, and loan amount against underwriting norms.",
                # Verbatim from spec 0031, drafted there and shipped as-is per the
                # user's "go ahead" — a genuine restoration, not new content.
                "system_prompt": (
                    "You are a credit risk officer at a community lender. You prioritize minimizing "
                    "default risk: weigh the applicant's DTI ratio, credit score, and loan amount "
                    "carefully against standard underwriting norms, and argue for caution or denial when "
                    "the numbers don't support a safe repayment outlook. Be specific about which figures "
                    "concern you. Be brief — 2-3 sentences."
                ),
                "model_config": GPT4O_MINI,
            },
        )

        relationship_loan_advisor, _ = AgentPersona.objects.get_or_create(
            name="Relationship Loan Advisor",
            role=AgentPersona.Role.PARTICIPANT,
            defaults={
                "role_description": "Looks for a legitimate, responsible path to loan approval.",
                # Verbatim from spec 0031 — a genuine restoration, not new content.
                "system_prompt": (
                    "You are a loan advisor focused on serving the customer relationship. You look for a "
                    "legitimate, responsible path to approval — compensating factors like collateral, a "
                    "strong income trend, or a smaller/restructured loan amount — while still respecting "
                    "the same underwriting norms as your counterpart. You don't ignore weak numbers, but "
                    "you argue for structuring a way to make a marginal case work when one reasonably "
                    "exists. Be brief — 2-3 sentences."
                ),
                "model_config": GPT4O_MINI,
            },
        )

        research_consultant, _ = AgentPersona.objects.get_or_create(
            name="Research Intake Consultant",
            role=AgentPersona.Role.CONSULTANT,
            defaults={
                "role_description": "Gathers an open-ended research or engineering question before it goes to debate.",
                "system_prompt": (
                    "You are a research intake consultant. Your job is to understand the question or "
                    "decision the user wants debated — help them articulate it clearly, ask clarifying "
                    "questions if the topic is vague, and confirm you've captured it accurately before "
                    "finalizing. This case type is fully open-ended — there's no fixed set of fields to "
                    "collect."
                ),
                "model_config": {"model": "gpt-4o-mini", "temperature": 0.5},
            },
        )

        loan_consultant, _ = AgentPersona.objects.get_or_create(
            name="Loan Intake Consultant",
            role=AgentPersona.Role.CONSULTANT,
            defaults={
                "role_description": "Gathers the information needed to evaluate a loan application before it goes to debate.",
                "system_prompt": (
                    "You are a loan intake consultant. Your job is to gather the information needed to "
                    "evaluate this loan application: the applicant's monthly income, monthly debt "
                    "payments, credit score, requested loan amount, and any collateral securing the loan. "
                    "Ask for whatever is missing, one or two things at a time, in a natural conversational "
                    "way. Once you have everything, confirm the details back to the applicant before "
                    "finalizing."
                ),
                "model_config": {"model": "gpt-4o-mini", "temperature": 0.5},
            },
        )

        research_debate, created = CaseTypeConfig.objects.get_or_create(
            type="research_debate",
            defaults={
                "position_options": [],
                "decision_options": [],
                "required_fields": [],
                "policy_context": "",
                "default_consultant_persona": research_consultant,
                "default_judge_persona": moderator,
            },
        )
        if created:
            research_debate.default_participant_personas.set([pragmatist, scale_minded])

        loan_approval, created = CaseTypeConfig.objects.get_or_create(
            type="loan_approval",
            defaults={
                # List order is the divergence->convergence spectrum (spec 0008) —
                # most-divergent first, most-convergent last, per TODO.md.
                "position_options": ["reject", "uncertain", "approve"],
                "decision_options": ["approve", "deny"],
                # Verbatim from spec 0030 — a genuine restoration, not new content.
                "required_fields": [
                    {"name": "monthly_income", "type": "number", "description": "Applicant's gross monthly income in USD"},
                    {"name": "monthly_debt", "type": "number", "description": "Applicant's total existing monthly debt payments in USD"},
                    {"name": "credit_score", "type": "number", "description": "Applicant's credit score (FICO)"},
                    {"name": "loan_amount", "type": "number", "description": "Requested loan amount in USD"},
                    {"name": "collateral", "type": "string", "description": "What secures the loan, if anything (or 'none')"},
                ],
                # Verbatim from spec 0031 — a genuine restoration, not new content.
                "policy_context": (
                    "Standard lending guidance for this case type: a debt-to-income (DTI) ratio above "
                    "45% is generally considered high risk without strong compensating factors (e.g. "
                    "substantial collateral, a co-signer, or a demonstrated income trend). Credit scores "
                    "below 620 typically warrant additional collateral or a smaller loan amount. A loan "
                    "amount that would push DTI above 50% should lean toward denial or restructuring "
                    "regardless of collateral, since it risks the applicant's ability to repay regardless "
                    "of security offered."
                ),
                "default_consultant_persona": loan_consultant,
                "default_judge_persona": moderator,
            },
        )
        if created:
            loan_approval.default_participant_personas.set([credit_risk_officer, relationship_loan_advisor])

        self.stdout.write(self.style.SUCCESS("Case types + personas seeded (or already present)."))
