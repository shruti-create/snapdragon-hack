package com.example.snap_app.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val FuelFormColorScheme = darkColorScheme(
    primary = FuelRed,
    secondary = FuelMagenta,
    tertiary = FuelBurgundy,
    background = DeepNavy,
    surface = CardDark,
    onPrimary = Color.White,
    onSecondary = Color.White,
    onTertiary = Color.White,
    onBackground = Color.White,
    onSurface = Color.White
)

@Composable
fun Snap_appTheme(
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = FuelFormColorScheme,
        typography = Typography,
        content = content
    )
}