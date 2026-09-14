# DataEngLab Claude Code Kit

Kit sans PHP pour générer :

- pages Elementor natives au format JSON ;
- cours compatibles Tutor LMS ;
- labs pratiques Data Engineering ;
- quiz, tests automatisés et solutions formateur ;
- ZIP étudiant séparé.

## Démarrage

1. Ajoutez votre export Elementor dans `references/elementor-reference.json`.
2. Ajoutez une capture de la home dans `references/homepage.png`.
3. Ouvrez ce dossier puis lancez `claude`.
4. Exécutez : `/create-course course-requests/airflow-pipeline.md`.

## Validation

```powershell
python scripts/run_checks.py output/airflow-pipeline
python scripts/package_student_lab.py output/airflow-pipeline
```
