#!/usr/bin/env python3
"""
Démonstration du module TaskManager
"""
from src.task_manager.manager import TaskManager
from src.task_manager.task import Priority, Status
from src.task_manager.services import EmailService

def main():
    print("=== Démonstration TaskManager ===\n")
    
    # On crée le gestionnaire de tâches
    manager = TaskManager("demo_tasks.json")
    
    # On ajoute plusieurs tâches avec des priorités différentes
    print("1. Ajout de tâches...")
    task1_id = manager.add_task("Finir le rapport", "Rapport mensuel à rendre", Priority.HIGH)
    task2_id = manager.add_task("Réunion équipe", "Réunion hebdomadaire", Priority.MEDIUM)
    task3_id = manager.add_task("Acheter du café", "Pour la machine du bureau", Priority.LOW)
    task4_id = manager.add_task("Préparer présentation", "Présentation client", Priority.URGENT)
    
    print(f"Tâches créées avec IDs: {task1_id[:8]}..., {task2_id[:8]}..., {task3_id[:8]}..., {task4_id[:8]}...")
    
    # On marque certaines tâches comme terminées
    print("\n2. Marquage de tâches comme terminées...")
    manager.get_task(task3_id).mark_completed()
    manager.get_task(task1_id).mark_completed()
    print("Tâches terminées: 'Acheter du café' et 'Finir le rapport'")
    
    # On affiche les statistiques
    print("\n3. Statistiques actuelles:")
    stats = manager.get_statistics()
    print(f"Total des tâches: {stats['total_tasks']}")
    print(f"Tâches terminées: {stats['completed_tasks']}")
    print(f"Tâches par priorité: {stats['tasks_by_priority']}")
    print(f"Tâches par statut: {stats['tasks_by_status']}")
    
    # On filtre les tâches par priorité et statut
    print("\n4. Filtrage des tâches:")
    urgent_tasks = manager.get_tasks_by_priority(Priority.URGENT)
    print(f"Tâches urgentes: {len(urgent_tasks)}")
    for task in urgent_tasks:
        print(f"  - {task.title}")
    
    todo_tasks = manager.get_tasks_by_status(Status.TODO)
    print(f"Tâches à faire: {len(todo_tasks)}")
    for task in todo_tasks:
        print(f"  - {task.title} (priorité: {task.priority.value})")
    
    # On sauvegarde les tâches dans un fichier
    print("\n5. Sauvegarde...")
    manager.save_to_file()
    print("Tâches sauvegardées dans 'demo_tasks.json'")
    
    # On recharge les tâches depuis le fichier
    print("\n6. Test de rechargement...")
    new_manager = TaskManager("demo_tasks.json")
    new_manager.load_from_file()
    print(f"Tâches rechargées: {len(new_manager.tasks)}")
    
    # On test le service email
    print("\n7. Test du service email...")
    email_service = EmailService()
    try:
        email_service.send_completion_notification("user@example.com", "Finir le rapport")
        print("Notification d'achèvement envoyée avec succès")
    except Exception as e:
        print(f"Erreur lors de l'envoi: {e}")
    
    print("\nDémo terminée avec succès !")

if __name__ == "__main__":
    main()