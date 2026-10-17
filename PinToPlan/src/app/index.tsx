
import { useState } from 'react';
import {
  SafeAreaView,
  View,
  Text,
  ScrollView,
  Image,
  Pressable,
  StyleSheet,
} from 'react-native';

const inspiration = [
  {
    id: '1',
    title: 'Outfit of the day',
    category: 'OUTFIT',
    time: '8:00 AM',
    image:
      'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=600',
  },
  {
    id: '2',
    title: 'Dinner inspiration',
    category: 'FOOD',
    time: '6:30 PM',
    image:
      'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=600',
  },
  {
    id: '3',
    title: 'Beauty inspiration',
    category: 'BEAUTY',
    time: '7:00 PM',
    image:
      'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=600',
  },
];

export default function HomeScreen() {
  const [selectedDay, setSelectedDay] = useState(20);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.brand}>dayboard.</Text>
        <Text style={styles.subtitle}>
          YOUR INSPIRATION, ON YOUR SCHEDULE
        </Text>

        <Text style={styles.heading}>Your week</Text>

        <View style={styles.week}>
          {[
            ['M', 19],
            ['T', 20],
            ['W', 21],
            ['T', 22],
            ['F', 23],
            ['S', 24],
            ['S', 25],
          ].map(([day, date]) => (
            <Pressable
              key={date}
              onPress={() => setSelectedDay(Number(date))}
              style={[
                styles.day,
                selectedDay === date && styles.selectedDay,
              ]}
            >
              <Text style={styles.dayLabel}>{day}</Text>
              <Text style={styles.dayNumber}>{date}</Text>
            </Pressable>
          ))}
        </View>

        <Text style={styles.heading}>
          {selectedDay === 20
            ? "Tuesday's inspiration"
            : `October ${selectedDay}`}
        </Text>

        <View style={styles.grid}>
          {inspiration.map((item) => (
            <View key={item.id} style={styles.card}>
              <Image
                source={{ uri: item.image }}
                style={styles.photo}
              />
              <Text style={styles.category}>
                {item.category}
              </Text>
              <Text style={styles.cardTitle}>{item.title}</Text>
              <Text style={styles.time}>{item.time}</Text>
            </View>
          ))}
        </View>

        <Pressable
          style={styles.addButton}
          onPress={() =>
            alert('Your Add Inspiration screen is next!')
          }
        >
          <Text style={styles.addButtonText}>
            + Add inspiration
          </Text>
        </Pressable>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FAF7F2',
  },
  content: {
    padding: 22,
    paddingBottom: 40,
  },
  brand: {
    fontSize: 32,
    fontWeight: '700',
    color: '#352F2A',
  },
  subtitle: {
    fontSize: 10,
    letterSpacing: 2,
    color: '#8B7B6E',
    marginTop: 5,
    marginBottom: 30,
  },
  heading: {
    fontSize: 21,
    fontWeight: '600',
    color: '#352F2A',
    marginBottom: 16,
    marginTop: 12,
  },
  week: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 24,
  },
  day: {
    padding: 9,
    borderRadius: 14,
    alignItems: 'center',
  },
  selectedDay: {
    backgroundColor: '#E6D8CA',
  },
  dayLabel: {
    color: '#88786A',
    fontSize: 12,
  },
  dayNumber: {
    fontSize: 15,
    fontWeight: '600',
    marginTop: 6,
    color: '#352F2A',
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  card: {
    width: '48%',
    marginBottom: 20,
  },
  photo: {
    width: '100%',
    aspectRatio: 0.78,
    borderRadius: 14,
    backgroundColor: '#E6D8CA',
  },
  category: {
    fontSize: 10,
    letterSpacing: 1.2,
    color: '#9B806B',
    marginTop: 9,
  },
  cardTitle: {
    fontSize: 15,
    fontWeight: '600',
    color: '#352F2A',
    marginTop: 4,
  },
  time: {
    fontSize: 12,
    color: '#88786A',
    marginTop: 4,
  },
  addButton: {
    backgroundColor: '#9B806B',
    borderRadius: 15,
    padding: 16,
    alignItems: 'center',
    marginTop: 8,
  },
  addButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
});
