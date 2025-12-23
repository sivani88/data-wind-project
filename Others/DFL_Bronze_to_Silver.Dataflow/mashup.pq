[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "wind_power_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared wind_power = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "00e69122-80e7-4974-8e82-5e52582fc33c"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "6267907f-fdb3-4ba4-90c0-7288faee2b34"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "wind_power", ItemKind = "Table"]}[Data],
  #"Rounded off" = Table.TransformColumns(#"Navigation 2", {{"production_id", each Number.Round(_, 2), type number}, {"wind_speed", each Number.Round(_, 2), type number}, {"energy_produced", each Number.Round(_, 2), type number}}),
  #"Inserted day" = Table.AddColumn(#"Rounded off", "Day", each Date.Day([date]), type nullable number),
  #"Changed column type" = Table.TransformColumnTypes(#"Inserted day", {{"Day", type date}, {"date", type date}}),
  #"Inserted month" = Table.AddColumn(#"Changed column type", "Month", each Date.Month([date]), type nullable number),
  #"Inserted quarter" = Table.AddColumn(#"Inserted month", "Quarter", each Date.QuarterOfYear([date]), type nullable number),
  #"Inserted year" = Table.AddColumn(#"Inserted quarter", "Year", each Date.Year([date]), type nullable number),
  #"Changed column type 1" = Table.TransformColumnTypes(#"Inserted year", {{"Day", type number}}),
  #"Removed columns" = Table.RemoveColumns(#"Changed column type 1", {"Day"}),
  #"Inserted day 1" = Table.AddColumn(#"Removed columns", "Day", each Date.Day([date]), type nullable number),
  #"Changed column type 2" = Table.TransformColumnTypes(#"Inserted day 1", {{"Month", Int64.Type}, {"Quarter", Int64.Type}, {"Year", Int64.Type}, {"Day", Int64.Type}}),
  #"Renamed columns" = Table.RenameColumns(#"Changed column type 2", {{"Month", "month"}, {"Quarter", "quarter"}, {"Year", "year"}, {"Day", "day"}}),
  #"Replaced value" = Table.ReplaceValue(#"Renamed columns", "-", ":", Replacer.ReplaceText, {"time"}),
  #"Duplicated column" = Table.DuplicateColumn(#"Replaced value", "time", "time - Copy"),
  #"Split column by delimiter" = Table.SplitColumn(#"Duplicated column", "time - Copy", Splitter.SplitTextByDelimiter(":"), {"time - Copy.1", "time - Copy.2", "time - Copy.3"}),
  #"Changed column type 3" = Table.TransformColumnTypes(#"Split column by delimiter", {{"time - Copy.1", Int64.Type}, {"time - Copy.2", Int64.Type}, {"time - Copy.3", Int64.Type}}),
  #"Renamed columns 1" = Table.RenameColumns(#"Changed column type 3", {{"time - Copy.1", "hour_of_day"}, {"time - Copy.2", "minute_of_hour"}, {"time - Copy.3", "seconde_of_minute"}}),
  #"Added custom" = Table.TransformColumnTypes(Table.AddColumn(#"Renamed columns 1", "TIME8PERIOD", each if [hour_of_day] >= 5 and [hour_of_day] <12 then "Morning"
else if  [hour_of_day] >= 12 and [hour_of_day] <17 then "Afternoon"
else if  [hour_of_day] >= 17 and [hour_of_day] <21 then "Afternoon"
else "Night"), {{"TIME8PERIOD", type text}})
in
  #"Added custom";
shared wind_power_DataDestination = let
  Pattern = Lakehouse.Contents([HierarchicalNavigation = null, CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "00e69122-80e7-4974-8e82-5e52582fc33c"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "69255059-660d-42ba-814d-5651d7c62dab"]}[Data],
  TableNavigation = Navigation_2{[Id = "wind_power", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
