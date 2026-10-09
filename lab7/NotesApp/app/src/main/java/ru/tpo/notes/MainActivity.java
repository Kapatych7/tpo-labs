package ru.tpo.notes;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.ArrayList;

/**
 * Приложение «Заметки ТПО» для ЛР7: добавление, удаление (долгое нажатие) и очистка заметок.
 * Заметки сохраняются в SharedPreferences, поэтому переживают поворот экрана,
 * сворачивание приложения и перезапуск.
 */
public class MainActivity extends AppCompatActivity {
    private static final String PREFS = "notes";
    private static final String KEY_NOTES = "items";

    private final ArrayList<String> notes = new ArrayList<>();
    private ArrayAdapter<String> adapter;
    private EditText input;
    private TextView counter;
    private TextView emptyText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        input = findViewById(R.id.noteInput);
        counter = findViewById(R.id.counterText);
        emptyText = findViewById(R.id.emptyText);
        Button addButton = findViewById(R.id.addButton);
        Button clearButton = findViewById(R.id.clearButton);
        ListView list = findViewById(R.id.notesList);

        loadNotes();
        adapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, notes);
        list.setAdapter(adapter);

        addButton.setOnClickListener(v -> addNote());
        clearButton.setOnClickListener(v -> {
            notes.clear();
            onNotesChanged();
        });
        list.setOnItemLongClickListener((parent, view, position, id) -> {
            notes.remove(position);
            onNotesChanged();
            Toast.makeText(this, R.string.deleted, Toast.LENGTH_SHORT).show();
            return true;
        });
        updateCounter();
    }

    private void addNote() {
        String text = input.getText().toString().trim();
        if (text.isEmpty()) {
            input.setError(getString(R.string.empty_error));
            return;
        }
        notes.add(0, text);
        input.setText("");
        onNotesChanged();
    }

    private void onNotesChanged() {
        adapter.notifyDataSetChanged();
        saveNotes();
        updateCounter();
    }

    private void updateCounter() {
        counter.setText(getString(R.string.counter, notes.size()));
        emptyText.setVisibility(notes.isEmpty() ? View.VISIBLE : View.GONE);
    }

    private void loadNotes() {
        SharedPreferences prefs = getSharedPreferences(PREFS, MODE_PRIVATE);
        try {
            JSONArray arr = new JSONArray(prefs.getString(KEY_NOTES, "[]"));
            for (int i = 0; i < arr.length(); i++) notes.add(arr.getString(i));
        } catch (JSONException e) {
            notes.clear();
        }
    }

    private void saveNotes() {
        getSharedPreferences(PREFS, MODE_PRIVATE).edit()
                .putString(KEY_NOTES, new JSONArray(notes).toString())
                .apply();
    }
}
