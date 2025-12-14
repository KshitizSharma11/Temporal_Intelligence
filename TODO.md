# TODO: Make Rules Accept Config via YAML Files

## Tasks
- [x] Create YAML config files for each rule (absence_rules.yaml, failed_login.yaml, correct_order_sequence.yaml) with parameters and severity
- [x] Modify AbsenceRules to accept config dict in __init__ and use severity in signals
- [x] Modify FailedLoginRule to accept config dict in __init__ and use severity in signals
- [x] Modify CorrectOrderSequenceRule to accept config dict in __init__ and use severity in signals
- [x] Update Engine to load YAML configs and pass to rules
- [x] Create async timer in app/infra/timer.py for absence rules
- [x] Remove check_timeouts from Engine and integrate with async timer
- [x] Test rule behavior with configs
