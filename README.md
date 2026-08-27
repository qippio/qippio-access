# Qippio Access

Qippio Access est une intégration Home Assistant permettant au client de contrôler l'accès distant du compte de maintenance Qippio.

## Fonctionnement

- Switch ON : accès distant Qippio autorisé
- Switch OFF : accès distant Qippio bloqué

L'intégration agit sur la propriété `local_only` du compte Home Assistant sélectionné comme compte Qippio.

## Installation

1. Installer Qippio Access via HACS.
2. Redémarrer Home Assistant.
3. Aller dans Paramètres > Appareils et services.
4. Ajouter l'intégration Qippio Access.
5. Sélectionner :
   - le compte Qippio
   - le compte client autorisé à contrôler l'accès
6. Ajouter l'entité `switch` au tableau de bord.
