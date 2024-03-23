import read_json as rj
from utils import get_keys_by_value
from icalendar import Calendar, Event
from datetime import datetime, timedelta


class TraductorCNF:
    def __init__(self, data):
        self.data = data
        self.teams = rj.get_teams(data)
        self.dates = rj.get_dates(data)
        self.hours = rj.get_hours(data)

    def match_generator(self):
        matches = {}
        match_count = 1

        for date in self.dates:
            for hour in self.hours:
                for local in self.teams:
                    for visitor in self.teams:
                        if local != visitor:
                            # Se crea las variables de los partidos
                            matches[(local, visitor, date, hour)] = match_count
                            match_count += 1

        return matches

    # restrictión 1: no se pueden jugar dos partidos al mismo tiempo
    def one_match(self, matches, clauses):
        for date in self.dates:
            for hour in self.hours:
                # Se obtienen los partidos que se juegan en la misma fecha y hora
                matches_date_hour = [
                    (local, visitor, date, hour)
                    for local in self.teams
                    for visitor in self.teams
                    if local != visitor
                ]

                # Se crea la cláusula
                for i, partido1 in enumerate(matches_date_hour):
                    for partido2 in matches_date_hour[i + 1 :]:
                        clause = [-matches[partido1], -matches[partido2]]
                        clauses.append(clause)

        return clauses

    # restricción 2: un equipo no puede jugar dos partidos el mismo día
    def one_team_one_day(self, matches, clauses):
        for date in self.dates:
            for team in self.teams:
                # Se obtienen los partidos de un equipo en la misma fecha
                matches_date_team = [
                    (local, visitor, date, hour)
                    for hour in self.hours
                    for local in self.teams
                    for visitor in self.teams
                    if local != visitor and (local == team or visitor == team)
                ]

                if len(matches_date_team) > 1:
                    # Se crea la cláusula
                    for i in range(len(matches_date_team)):
                        for j in range(i + 1, len(matches_date_team)):
                            clause = [
                                -matches[matches_date_team[i]],
                                -matches[matches_date_team[j]],
                            ]
                            clauses.append(clause)

        return clauses

    # restricción 3: un equipo no puede jugar como local dias consecutivos o como visitante dias consecutivos
    def one_team_consecutive_days(self, matches, clauses):
        for team in self.teams:
            for i in range(len(self.dates) - 1):
                actual_date = self.dates[i]
                next_date = self.dates[i + 1]

                # Se obtienen los partidos de un equipo en la fecha actual y la siguiente de local
                matches_local = [
                    (team, visitor, actual_date, hour)
                    for hour in self.hours
                    for visitor in self.teams
                    if team != visitor
                ]

                next_matches_local = [
                    (team, visitor, next_date, hour)
                    for hour in self.hours
                    for visitor in self.teams
                    if team != visitor
                ]

                # Se obtienen los partidos de un equipo en la fecha actual y la siguiente de visitante
                matches_visitor = [
                    (local, team, actual_date, hour)
                    for hour in self.hours
                    for local in self.teams
                    if local != team
                ]

                next_matches_visitor = [
                    (local, team, next_date, hour)
                    for hour in self.hours
                    for local in self.teams
                    if local != team
                ]

                # Se crea la cláusula que impide que un equipo juegue dos partidos seguidos de local
                for match_actual in matches_local:
                    for match_next in next_matches_local:
                        clause = [-matches[match_actual], -matches[match_next]]
                        clauses.append(clause)

                # Se crea la cláusula que impide que un equipo juegue dos partidos seguidos de visitante
                for match_actual in matches_visitor:
                    for match_next in next_matches_visitor:
                        clause = [-matches[match_actual], -matches[match_next]]
                        clauses.append(clause)

        return clauses

    # restricción 4: un equipo juega exactamente una vez como local y una vez como visitante con cada equipo
    def one_team_one_opponent(self, matches, clauses):
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                team = self.teams[i]
                opponent = self.teams[j]

                # Se obtienen los partidos del team contra el opponent como local
                matches_local = [
                    matches[(team, opponent, date, hour)]
                    for date in self.dates
                    for hour in self.hours
                ]

                # Se obtienen los partidos del team contra el opponent como visitante
                matches_visitor = [
                    matches[(opponent, team, date, hour)]
                    for date in self.dates
                    for hour in self.hours
                ]

                # Se crea la cláusula que impide que el team juegue más de una vez como local contra el opponent
                clauses += self.only_one(matches_local)

                # Se crea la cláusula que impide que el team juegue más de una vez como visitante contra el opponent
                clauses += self.only_one(matches_visitor)

        return clauses

    def only_one(self, match_number):
        clauses = []

        # Al menos un partido ocurre
        clauses.append([match for match in match_number])

        # A lo sumo un partido ocurre
        for i in range(len(match_number)):
            for j in range(i + 1, len(match_number)):
                clauses.append([-match_number[i], -match_number[j]])

        return clauses

    def cnf_clause(self):
        clauses = []
        matches = self.match_generator()

        # restricción 1: no se pueden jugar dos partidos al mismo tiempo
        clauses = self.one_match(matches, clauses)

        # restricción 2: un equipo no puede jugar dos partidos el mismo día
        clauses = self.one_team_one_day(matches, clauses)

        # restricción 3: un equipo no puede jugar como local dias consecutivos o como visitante dias consecutivos
        clauses = self.one_team_consecutive_days(matches, clauses)

        # restricción 4: un equipo juega exactamente una vez como local y una vez como visitante con cada equipo
        clauses = self.one_team_one_opponent(matches, clauses)

        return clauses

    # crea el archivo en formato dimacs cnf
    def dismacs(self, var_count, clauses, file_name):
        with open("{}.dimacs".format(file_name), "w") as file:
            file.write("p cnf {} {}\n".format(var_count, len(clauses)))
            for clause in clauses:
                file.write(" ".join(map(str, clause)) + " 0\n")

    # crea el archivo .ics
    def ical(self, solution):
        cal = Calendar()
        cal.add("prodid", "-//My calendar product//example.com//")
        cal.add("version", "2.0")
        cal.add("name", rj.get_tournament_name(self.data))

        maches = self.match_generator()
        for sol in solution.split():
            if int(sol) > 0:
                var = get_keys_by_value(maches, int(sol))

                j1 = var[0][0]
                j2 = var[0][1]
                d = var[0][2]
                hi = var[0][3]
                hf = (
                    datetime.strptime(f"{d} {hi}", "%Y-%m-%d %H:%M:%S")
                    + timedelta(hours=2)
                ).time()

                event = Event()
                event.add("summary", f"{j1} vs {j2}")
                event.add(
                    "dtstart", datetime.strptime(f"{d} {hi}", "%Y-%m-%d %H:%M:%S")
                )
                event.add("dtend", datetime.strptime(f"{d} {hf}", "%Y-%m-%d %H:%M:%S"))
                cal.add_component(event)

        # write .ics file
        f = open(f"{rj.get_tournament_name(self.data).lower()}.ics", "wb")
        f.write(cal.to_ical())
        f.close()
