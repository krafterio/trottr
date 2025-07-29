import cli
from rich.console import Console
from cli.commands.db import db
from core.app import CliApp
from models.country import Country
from models.service_plan import ServicePlan, ServicePlanPeriod, ServicePlanType
from models.service_tax import ServiceTax

console = Console()


@db.command()
@cli.pass_app
async def init_data(app: CliApp):
    """Init the database"""
    async with app.lifespan():
        await initialize_subscription_plans()
        await initialize_subscription_taxes()
        await initialize_countries()
        console.print(f"[green]Database is initialized with successfully[/green]")


async def initialize_subscription_plans():
    """Initialize the subscription plans"""
    plan_definitions = [
        # Pro
        {
            "name": "Trottr Essential Mensuel",
            "type": ServicePlanType.essential,
            "period": ServicePlanPeriod.monthly,
            "price": 59.00,
            "currency": "EUR",
            "description": None,
        },
        {
            "name": "Trottr Essential Annuel",
            "type": ServicePlanType.essential,
            "period": ServicePlanPeriod.yearly,
            "price": 12 * 49.00,
            "currency": "EUR",
            "description": None,
        },
        # Team
        {
            "name": "Trottr Advanced Mensuel",
            "type": ServicePlanType.advanced,
            "period": ServicePlanPeriod.monthly,
            "price": 89.00,
            "currency": "EUR",
            "description": None,
        },
        {
            "name": "Trottr Advanced Annuel",
            "type": ServicePlanType.advanced,
            "period": ServicePlanPeriod.yearly,
            "price": 12 * 79.00,
            "currency": "EUR",
            "description": None,
        },
        # Enterprise
        {
            "name": "Trottr Business Mensuel",
            "type": ServicePlanType.business,
            "period": ServicePlanPeriod.monthly,
            "price": 119.00,
            "currency": "EUR",
            "description": None,
        },
        {
            "name": "Trottr Business Annuel",
            "type": ServicePlanType.business,
            "period": ServicePlanPeriod.yearly,
            "price": 12 * 99.00,
            "currency": "EUR",
            "description": None,
        },
    ]

    console.print("[bold]Initializing subscription plans...[/bold]")

    for definition in plan_definitions:
        existing_plan = await ServicePlan.query.filter(
            type=definition["type"],
            period=definition["period"]
        ).first()

        if existing_plan:
            console.print(f"  [yellow]Existing plan '{definition['name']}' - ignored[/yellow]")
            continue

        plan = await ServicePlan.query.create(
            name=definition["name"],
            type=definition["type"],
            period=definition["period"],
            price=definition["price"],
            currency=definition["currency"],
            description=definition["description"],
            is_active=True,
        )

        console.print(f"  [green]Plan '{plan.name}' created with successfully[/green]")


async def initialize_subscription_taxes():
    """Initialize the subscription taxes"""
    tax_definitions = [
        # France
        {
            "name": "TVA 20%",
            "rate": 20.0,
            "country_code": "FR",
            "description": None,
        },
    ]

    console.print("[bold]Initializing subscription taxes...[/bold]")

    for definition in tax_definitions:
        existing_tax = await ServiceTax.query.filter(
            rate=definition["rate"],
            country_code=definition["country_code"],
        ).first()

        if existing_tax:
            console.print(f"  [yellow]Existing tax '{definition['name']}' - ignored[/yellow]")
            continue

        tax = await ServiceTax.query.create(
            name=definition["name"],
            rate=definition["rate"],
            country_code=definition["country_code"],
            description=definition["description"],
            is_active=True,
        )

        console.print(f"  [green]Tax '{tax.name}' created with successfully[/green]")


async def initialize_countries():
    """Initialize all countries with their ISO codes"""
    countries_definitions = [
        {"name": "Afghanistan", "iso_code": "AF"},
        {"name": "Îles Åland", "iso_code": "AX"},
        {"name": "Albanie", "iso_code": "AL"},
        {"name": "Algérie", "iso_code": "DZ"},
        {"name": "Samoa américaines", "iso_code": "AS"},
        {"name": "Andorre", "iso_code": "AD"},
        {"name": "Angola", "iso_code": "AO"},
        {"name": "Anguilla", "iso_code": "AI"},
        {"name": "Antarctique", "iso_code": "AQ"},
        {"name": "Antigua-et-Barbuda", "iso_code": "AG"},
        {"name": "Argentine", "iso_code": "AR"},
        {"name": "Arménie", "iso_code": "AM"},
        {"name": "Aruba", "iso_code": "AW"},
        {"name": "Australie", "iso_code": "AU"},
        {"name": "Autriche", "iso_code": "AT"},
        {"name": "Azerbaïdjan", "iso_code": "AZ"},
        {"name": "Bahamas", "iso_code": "BS"},
        {"name": "Bahreïn", "iso_code": "BH"},
        {"name": "Bangladesh", "iso_code": "BD"},
        {"name": "Barbade", "iso_code": "BB"},
        {"name": "Biélorussie", "iso_code": "BY"},
        {"name": "Belgique", "iso_code": "BE"},
        {"name": "Belize", "iso_code": "BZ"},
        {"name": "Bénin", "iso_code": "BJ"},
        {"name": "Bermudes", "iso_code": "BM"},
        {"name": "Bhoutan", "iso_code": "BT"},
        {"name": "Bolivie", "iso_code": "BO"},
        {"name": "Bonaire, Saint-Eustache et Saba", "iso_code": "BQ"},
        {"name": "Bosnie-Herzégovine", "iso_code": "BA"},
        {"name": "Botswana", "iso_code": "BW"},
        {"name": "Île Bouvet", "iso_code": "BV"},
        {"name": "Brésil", "iso_code": "BR"},
        {"name": "Territoire britannique de l'océan Indien", "iso_code": "IO"},
        {"name": "Brunei", "iso_code": "BN"},
        {"name": "Bulgarie", "iso_code": "BG"},
        {"name": "Burkina Faso", "iso_code": "BF"},
        {"name": "Burundi", "iso_code": "BI"},
        {"name": "Cap-Vert", "iso_code": "CV"},
        {"name": "Cambodge", "iso_code": "KH"},
        {"name": "Cameroun", "iso_code": "CM"},
        {"name": "Canada", "iso_code": "CA"},
        {"name": "Îles Caïmans", "iso_code": "KY"},
        {"name": "République centrafricaine", "iso_code": "CF"},
        {"name": "Tchad", "iso_code": "TD"},
        {"name": "Chili", "iso_code": "CL"},
        {"name": "Chine", "iso_code": "CN"},
        {"name": "Île Christmas", "iso_code": "CX"},
        {"name": "Îles Cocos", "iso_code": "CC"},
        {"name": "Colombie", "iso_code": "CO"},
        {"name": "Comores", "iso_code": "KM"},
        {"name": "Congo", "iso_code": "CG"},
        {"name": "République démocratique du Congo", "iso_code": "CD"},
        {"name": "Îles Cook", "iso_code": "CK"},
        {"name": "Costa Rica", "iso_code": "CR"},
        {"name": "Côte d'Ivoire", "iso_code": "CI"},
        {"name": "Croatie", "iso_code": "HR"},
        {"name": "Cuba", "iso_code": "CU"},
        {"name": "Curaçao", "iso_code": "CW"},
        {"name": "Chypre", "iso_code": "CY"},
        {"name": "République tchèque", "iso_code": "CZ"},
        {"name": "Danemark", "iso_code": "DK"},
        {"name": "Djibouti", "iso_code": "DJ"},
        {"name": "Dominique", "iso_code": "DM"},
        {"name": "République dominicaine", "iso_code": "DO"},
        {"name": "Équateur", "iso_code": "EC"},
        {"name": "Égypte", "iso_code": "EG"},
        {"name": "Salvador", "iso_code": "SV"},
        {"name": "Guinée équatoriale", "iso_code": "GQ"},
        {"name": "Érythrée", "iso_code": "ER"},
        {"name": "Estonie", "iso_code": "EE"},
        {"name": "Eswatini", "iso_code": "SZ"},
        {"name": "Éthiopie", "iso_code": "ET"},
        {"name": "Îles Malouines", "iso_code": "FK"},
        {"name": "Îles Féroé", "iso_code": "FO"},
        {"name": "Fidji", "iso_code": "FJ"},
        {"name": "Finlande", "iso_code": "FI"},
        {"name": "France", "iso_code": "FR"},
        {"name": "Guyane française", "iso_code": "GF"},
        {"name": "Polynésie française", "iso_code": "PF"},
        {"name": "Terres australes françaises", "iso_code": "TF"},
        {"name": "Gabon", "iso_code": "GA"},
        {"name": "Gambie", "iso_code": "GM"},
        {"name": "Géorgie", "iso_code": "GE"},
        {"name": "Allemagne", "iso_code": "DE"},
        {"name": "Ghana", "iso_code": "GH"},
        {"name": "Gibraltar", "iso_code": "GI"},
        {"name": "Grèce", "iso_code": "GR"},
        {"name": "Groenland", "iso_code": "GL"},
        {"name": "Grenade", "iso_code": "GD"},
        {"name": "Guadeloupe", "iso_code": "GP"},
        {"name": "Guam", "iso_code": "GU"},
        {"name": "Guatemala", "iso_code": "GT"},
        {"name": "Guernesey", "iso_code": "GG"},
        {"name": "Guinée", "iso_code": "GN"},
        {"name": "Guinée-Bissau", "iso_code": "GW"},
        {"name": "Guyana", "iso_code": "GY"},
        {"name": "Haïti", "iso_code": "HT"},
        {"name": "Îles Heard-et-MacDonald", "iso_code": "HM"},
        {"name": "Saint-Siège", "iso_code": "VA"},
        {"name": "Honduras", "iso_code": "HN"},
        {"name": "Hong Kong", "iso_code": "HK"},
        {"name": "Hongrie", "iso_code": "HU"},
        {"name": "Islande", "iso_code": "IS"},
        {"name": "Inde", "iso_code": "IN"},
        {"name": "Indonésie", "iso_code": "ID"},
        {"name": "Iran", "iso_code": "IR"},
        {"name": "Irak", "iso_code": "IQ"},
        {"name": "Irlande", "iso_code": "IE"},
        {"name": "Île de Man", "iso_code": "IM"},
        {"name": "Israël", "iso_code": "IL"},
        {"name": "Italie", "iso_code": "IT"},
        {"name": "Jamaïque", "iso_code": "JM"},
        {"name": "Japon", "iso_code": "JP"},
        {"name": "Jersey", "iso_code": "JE"},
        {"name": "Jordanie", "iso_code": "JO"},
        {"name": "Kazakhstan", "iso_code": "KZ"},
        {"name": "Kenya", "iso_code": "KE"},
        {"name": "Kiribati", "iso_code": "KI"},
        {"name": "Corée du Nord", "iso_code": "KP"},
        {"name": "Corée du Sud", "iso_code": "KR"},
        {"name": "Koweït", "iso_code": "KW"},
        {"name": "Kirghizistan", "iso_code": "KG"},
        {"name": "Laos", "iso_code": "LA"},
        {"name": "Lettonie", "iso_code": "LV"},
        {"name": "Liban", "iso_code": "LB"},
        {"name": "Lesotho", "iso_code": "LS"},
        {"name": "Libéria", "iso_code": "LR"},
        {"name": "Libye", "iso_code": "LY"},
        {"name": "Liechtenstein", "iso_code": "LI"},
        {"name": "Lituanie", "iso_code": "LT"},
        {"name": "Luxembourg", "iso_code": "LU"},
        {"name": "Macao", "iso_code": "MO"},
        {"name": "Madagascar", "iso_code": "MG"},
        {"name": "Malawi", "iso_code": "MW"},
        {"name": "Malaisie", "iso_code": "MY"},
        {"name": "Maldives", "iso_code": "MV"},
        {"name": "Mali", "iso_code": "ML"},
        {"name": "Malte", "iso_code": "MT"},
        {"name": "Îles Marshall", "iso_code": "MH"},
        {"name": "Martinique", "iso_code": "MQ"},
        {"name": "Mauritanie", "iso_code": "MR"},
        {"name": "Maurice", "iso_code": "MU"},
        {"name": "Mayotte", "iso_code": "YT"},
        {"name": "Mexique", "iso_code": "MX"},
        {"name": "Micronésie", "iso_code": "FM"},
        {"name": "Moldavie", "iso_code": "MD"},
        {"name": "Monaco", "iso_code": "MC"},
        {"name": "Mongolie", "iso_code": "MN"},
        {"name": "Monténégro", "iso_code": "ME"},
        {"name": "Montserrat", "iso_code": "MS"},
        {"name": "Maroc", "iso_code": "MA"},
        {"name": "Mozambique", "iso_code": "MZ"},
        {"name": "Myanmar", "iso_code": "MM"},
        {"name": "Namibie", "iso_code": "NA"},
        {"name": "Nauru", "iso_code": "NR"},
        {"name": "Népal", "iso_code": "NP"},
        {"name": "Pays-Bas", "iso_code": "NL"},
        {"name": "Nouvelle-Calédonie", "iso_code": "NC"},
        {"name": "Nouvelle-Zélande", "iso_code": "NZ"},
        {"name": "Nicaragua", "iso_code": "NI"},
        {"name": "Niger", "iso_code": "NE"},
        {"name": "Nigéria", "iso_code": "NG"},
        {"name": "Niue", "iso_code": "NU"},
        {"name": "Île Norfolk", "iso_code": "NF"},
        {"name": "Macédoine du Nord", "iso_code": "MK"},
        {"name": "Îles Mariannes du Nord", "iso_code": "MP"},
        {"name": "Norvège", "iso_code": "NO"},
        {"name": "Oman", "iso_code": "OM"},
        {"name": "Pakistan", "iso_code": "PK"},
        {"name": "Palaos", "iso_code": "PW"},
        {"name": "Palestine", "iso_code": "PS"},
        {"name": "Panama", "iso_code": "PA"},
        {"name": "Papouasie-Nouvelle-Guinée", "iso_code": "PG"},
        {"name": "Paraguay", "iso_code": "PY"},
        {"name": "Pérou", "iso_code": "PE"},
        {"name": "Philippines", "iso_code": "PH"},
        {"name": "Îles Pitcairn", "iso_code": "PN"},
        {"name": "Pologne", "iso_code": "PL"},
        {"name": "Portugal", "iso_code": "PT"},
        {"name": "Porto Rico", "iso_code": "PR"},
        {"name": "Qatar", "iso_code": "QA"},
        {"name": "La Réunion", "iso_code": "RE"},
        {"name": "Roumanie", "iso_code": "RO"},
        {"name": "Russie", "iso_code": "RU"},
        {"name": "Rwanda", "iso_code": "RW"},
        {"name": "Saint-Barthélemy", "iso_code": "BL"},
        {"name": "Sainte-Hélène", "iso_code": "SH"},
        {"name": "Saint-Kitts-et-Nevis", "iso_code": "KN"},
        {"name": "Sainte-Lucie", "iso_code": "LC"},
        {"name": "Saint-Martin", "iso_code": "MF"},
        {"name": "Saint-Pierre-et-Miquelon", "iso_code": "PM"},
        {"name": "Saint-Vincent-et-les-Grenadines", "iso_code": "VC"},
        {"name": "Samoa", "iso_code": "WS"},
        {"name": "Saint-Marin", "iso_code": "SM"},
        {"name": "Sao Tomé-et-Principe", "iso_code": "ST"},
        {"name": "Arabie saoudite", "iso_code": "SA"},
        {"name": "Sénégal", "iso_code": "SN"},
        {"name": "Serbie", "iso_code": "RS"},
        {"name": "Seychelles", "iso_code": "SC"},
        {"name": "Sierra Leone", "iso_code": "SL"},
        {"name": "Singapour", "iso_code": "SG"},
        {"name": "Sint Maarten", "iso_code": "SX"},
        {"name": "Slovaquie", "iso_code": "SK"},
        {"name": "Slovénie", "iso_code": "SI"},
        {"name": "Îles Salomon", "iso_code": "SB"},
        {"name": "Somalie", "iso_code": "SO"},
        {"name": "Afrique du Sud", "iso_code": "ZA"},
        {"name": "Géorgie du Sud-et-les Îles Sandwich du Sud", "iso_code": "GS"},
        {"name": "Soudan du Sud", "iso_code": "SS"},
        {"name": "Espagne", "iso_code": "ES"},
        {"name": "Sri Lanka", "iso_code": "LK"},
        {"name": "Soudan", "iso_code": "SD"},
        {"name": "Suriname", "iso_code": "SR"},
        {"name": "Svalbard et Jan Mayen", "iso_code": "SJ"},
        {"name": "Suède", "iso_code": "SE"},
        {"name": "Suisse", "iso_code": "CH"},
        {"name": "Syrie", "iso_code": "SY"},
        {"name": "Taïwan", "iso_code": "TW"},
        {"name": "Tadjikistan", "iso_code": "TJ"},
        {"name": "Tanzanie", "iso_code": "TZ"},
        {"name": "Thaïlande", "iso_code": "TH"},
        {"name": "Timor oriental", "iso_code": "TL"},
        {"name": "Togo", "iso_code": "TG"},
        {"name": "Tokelau", "iso_code": "TK"},
        {"name": "Tonga", "iso_code": "TO"},
        {"name": "Trinité-et-Tobago", "iso_code": "TT"},
        {"name": "Tunisie", "iso_code": "TN"},
        {"name": "Turquie", "iso_code": "TR"},
        {"name": "Turkménistan", "iso_code": "TM"},
        {"name": "Îles Turques-et-Caïques", "iso_code": "TC"},
        {"name": "Tuvalu", "iso_code": "TV"},
        {"name": "Ouganda", "iso_code": "UG"},
        {"name": "Ukraine", "iso_code": "UA"},
        {"name": "Émirats arabes unis", "iso_code": "AE"},
        {"name": "Royaume-Uni", "iso_code": "GB"},
        {"name": "États-Unis", "iso_code": "US"},
        {"name": "Îles mineures éloignées des États-Unis", "iso_code": "UM"},
        {"name": "Uruguay", "iso_code": "UY"},
        {"name": "Ouzbékistan", "iso_code": "UZ"},
        {"name": "Vanuatu", "iso_code": "VU"},
        {"name": "Venezuela", "iso_code": "VE"},
        {"name": "Viêt Nam", "iso_code": "VN"},
        {"name": "Îles Vierges britanniques", "iso_code": "VG"},
        {"name": "Îles Vierges américaines", "iso_code": "VI"},
        {"name": "Wallis-et-Futuna", "iso_code": "WF"},
        {"name": "Sahara occidental", "iso_code": "EH"},
        {"name": "Yémen", "iso_code": "YE"},
        {"name": "Zambie", "iso_code": "ZM"},
        {"name": "Zimbabwe", "iso_code": "ZW"},
    ]

    console.print("[bold]Initializing countries...[/bold]")

    for definition in countries_definitions:
        existing_country = await Country.query.filter(
            iso_code=definition["iso_code"]
        ).first()

        if existing_country:
            console.print(f"  [yellow]Existing country '{definition['name']}' ({definition['iso_code']}) - ignored[/yellow]")
            continue

        country = await Country.query.create(
            name=definition["name"],
            iso_code=definition["iso_code"],
        )

        console.print(f"  [green]Country '{country.name}' ({country.iso_code}) created successfully[/green]")
