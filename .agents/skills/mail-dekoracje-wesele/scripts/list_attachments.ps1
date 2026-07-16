param(
    [string]$DecorationsDir = "raw/dekoracje",
    [string]$ExcludedFileName = "przystanek_poludnie.jpg"
)

$resolvedDir = Resolve-Path -LiteralPath $DecorationsDir -ErrorAction Stop

Get-ChildItem -LiteralPath $resolvedDir -File |
    Where-Object { $_.Name -ne $ExcludedFileName } |
    Sort-Object Name |
    ForEach-Object { $_.FullName }
