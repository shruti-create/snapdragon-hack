package com.example.snap_app

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

// Data Classes
data class ChatMessage(
    val id: String = UUID.randomUUID().toString(),
    val content: String,
    val isUser: Boolean,
    val timestamp: Long = System.currentTimeMillis()
)

@Composable
fun ChatScreen() {
    var messages by remember { mutableStateOf(listOf<ChatMessage>()) }
    var messageText by remember { mutableStateOf("") }
    var isTyping by remember { mutableStateOf(false) }
    val listState = rememberLazyListState()
    val coroutineScope = rememberCoroutineScope()

    // Template responses
    val templates = listOf(
        "Tell me about my workout plan",
        "What should I eat today?",
        "How many calories should I consume?",
        "Give me fitness tips",
        "Track my progress"
    )

    // AI responses based on user input
    val aiResponses = mapOf(
        "workout" to "Great question! Based on your profile, you should focus on strength training 3-4 times per week. Make sure to include compound exercises like squats, deadlifts, and bench press for maximum results! 💪",
        "eat" to "For today, I recommend following your Week 1 meal plan: Oatmeal with berries for breakfast, grilled chicken salad for lunch, and salmon with roasted vegetables for dinner. This will keep you at your target calorie intake! 🍎",
        "calories" to "Based on your TDEE calculation, you should aim for around 2,200-2,400 calories per day to meet your fitness goals. Make sure to balance your macros: 40% carbs, 30% protein, 30% fats! 📊",
        "tips" to "Here are some quick fitness tips: 1) Stay hydrated - drink at least 8 glasses of water daily 💧 2) Get 7-9 hours of sleep 😴 3) Don't skip warm-ups 🔥 4) Progressive overload is key 📈 5) Rest days are important for recovery! ✨",
        "progress" to "You're doing amazing! You've completed 65% of your workouts this week and stayed within your calorie goals for 5 out of 7 days. Keep up the excellent work! 🎉",
        "hello" to "Hey there! 👋 I'm here to help you with your fitness and nutrition journey. What would you like to know?",
        "help" to "I can help you with:\n• Workout plans and exercises\n• Nutrition and meal planning\n• Calorie tracking\n• Fitness tips and motivation\n• Progress tracking\n\nWhat do you need help with? 😊"
    )

    // Initial greeting
    LaunchedEffect(Unit) {
        messages = listOf(
            ChatMessage(
                content = "Hi! 👋 I'm your AI fitness assistant. I'm here to help you achieve your fitness goals! How can I assist you today?",
                isUser = false
            )
        )
    }

    // Auto-scroll to bottom when new messages arrive
    LaunchedEffect(messages.size) {
        if (messages.isNotEmpty()) {
            listState.animateScrollToItem(messages.size - 1)
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp)
    ) {
        Column(
            modifier = Modifier.fillMaxSize()
        ) {
            // Header
            Text(
                text = "AI Assistant 🤖",
                style = MaterialTheme.typography.headlineMedium,
                color = NeonPink,
                fontWeight = FontWeight.Bold
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = "Your personal fitness companion",
                style = MaterialTheme.typography.bodyMedium,
                color = Color.White.copy(alpha = 0.8f)
            )

            Spacer(modifier = Modifier.height(24.dp))

            // Messages List
            LazyColumn(
                state = listState,
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(messages) { message ->
                    MessageBubble(message)
                }

                // Typing indicator
                if (isTyping) {
                    item {
                        TypingIndicator()
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Template responses (quick replies)
            if (messages.size <= 2) {
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    items(templates) { template ->
                        TemplateChip(
                            text = template,
                            onClick = {
                                if (messageText.isEmpty()) {
                                    messageText = template
                                }
                            }
                        )
                    }
                }
                Spacer(modifier = Modifier.height(12.dp))
            }

            // Input Field
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                TextField(
                    value = messageText,
                    onValueChange = { messageText = it },
                    modifier = Modifier
                        .weight(1f),
                    placeholder = {
                        Text(
                            text = "Type a message...",
                            color = Color.Gray
                        )
                    },
                    colors = TextFieldDefaults.colors(
                        focusedContainerColor = Color(0xFF2A2A2A),
                        unfocusedContainerColor = Color(0xFF2A2A2A),
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White,
                        cursorColor = NeonPink,
                        focusedIndicatorColor = Color.Transparent,
                        unfocusedIndicatorColor = Color.Transparent
                    ),
                    shape = RoundedCornerShape(24.dp),
                    maxLines = 3
                )

                // Send Button
                IconButton(
                    onClick = {
                        if (messageText.isNotBlank()) {
                            // Add user message
                            val userMessage = ChatMessage(
                                content = messageText,
                                isUser = true
                            )
                            messages = messages + userMessage

                            val userInput = messageText.lowercase()
                            messageText = ""

                            // Show typing indicator
                            isTyping = true

                            // Simulate AI response delay
                            coroutineScope.launch {
                                delay(1500)
                                isTyping = false

                                // Find matching AI response
                                val aiResponse = aiResponses.entries.find {
                                    userInput.contains(it.key)
                                }?.value ?: "I understand you're asking about '$userInput'. While I don't have a specific answer for that, I'm here to help with your fitness journey! Try asking about workouts, nutrition, or your progress. 💪"

                                val aiMessage = ChatMessage(
                                    content = aiResponse,
                                    isUser = false
                                )
                                messages = messages + aiMessage
                            }
                        }
                    },
                    modifier = Modifier
                        .size(56.dp)
                        .background(
                            color = if (messageText.isNotBlank()) NeonPink else Color.Gray,
                            shape = CircleShape
                        ),
                    enabled = messageText.isNotBlank()
                ) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.Send,
                        contentDescription = "Send",
                        tint = Color.White
                    )
                }
            }
        }
    }
}

@Composable
fun MessageBubble(message: ChatMessage) {
    val alignment = if (message.isUser) Alignment.End else Alignment.Start
    val backgroundColor = if (message.isUser) NeonPink else Color(0xFF2A2A2A)
    val textColor = Color.White

    val timeFormat = SimpleDateFormat("HH:mm", Locale.getDefault())
    val timeString = timeFormat.format(Date(message.timestamp))

    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = alignment
    ) {
        Box(
            modifier = Modifier
                .widthIn(max = 280.dp)
                .background(
                    color = backgroundColor,
                    shape = RoundedCornerShape(
                        topStart = 16.dp,
                        topEnd = 16.dp,
                        bottomStart = if (message.isUser) 16.dp else 4.dp,
                        bottomEnd = if (message.isUser) 4.dp else 16.dp
                    )
                )
                .padding(12.dp)
        ) {
            Column {
                Text(
                    text = message.content,
                    color = textColor,
                    fontSize = 15.sp,
                    lineHeight = 20.sp
                )

                Spacer(modifier = Modifier.height(4.dp))

                Text(
                    text = timeString,
                    color = textColor.copy(alpha = 0.6f),
                    fontSize = 11.sp,
                    modifier = Modifier.align(Alignment.End)
                )
            }
        }
    }
}

@Composable
fun TemplateChip(
    text: String,
    onClick: () -> Unit
) {
    Box(
        modifier = Modifier
            .background(
                color = Color(0xFF2A2A2A),
                shape = RoundedCornerShape(20.dp)
            )
            .clickable { onClick() }
            .padding(horizontal = 16.dp, vertical = 10.dp)
    ) {
        Text(
            text = text,
            color = NeonPink,
            fontSize = 13.sp,
            fontWeight = FontWeight.Medium
        )
    }
}

@Composable
fun TypingIndicator() {
    Row(
        modifier = Modifier
            .widthIn(max = 80.dp)
            .background(
                color = Color(0xFF2A2A2A),
                shape = RoundedCornerShape(
                    topStart = 16.dp,
                    topEnd = 16.dp,
                    bottomStart = 4.dp,
                    bottomEnd = 16.dp
                )
            )
            .padding(16.dp),
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        repeat(3) { index ->
            val alpha by animateFloatAsState(
                targetValue = if ((System.currentTimeMillis() / 400) % 3 == index.toLong()) 1f else 0.3f,
                label = "dot_$index"
            )
            Box(
                modifier = Modifier
                    .size(8.dp)
                    .background(
                        color = Color.White.copy(alpha = alpha),
                        shape = CircleShape
                    )
            )
        }
    }
}

@Composable
private fun animateFloatAsState(targetValue: Float, label: String): State<Float> {
    return remember { mutableStateOf(targetValue) }
}