// Create a blank query named PayrollSource and paste this into Advanced Editor.
// Set server/database for your own LOCAL machine; authenticate in Power BI's credential dialog.
let
    Server = "localhost:15432",
    Database = "payroll",
    Source = PostgreSQL.Database(Server, Database, [CreateNavigationProperties=false]),
    Tables = [
        dim_department = Source{[Schema="payroll_analytics", Item="dim_department"]}[Data],
        dim_location = Source{[Schema="payroll_analytics", Item="dim_location"]}[Data],
        dim_employee = Source{[Schema="payroll_analytics", Item="dim_employee"]}[Data],
        dim_snapshot = Source{[Schema="payroll_analytics", Item="dim_snapshot"]}[Data],
        fact_compensation = Source{[Schema="payroll_analytics", Item="bi_fact_compensation"]}[Data]
    ]
in
    Tables
