import simpy
import random
import numpy as np
import math


# Distribution related parameters initialized.
INTERARRIVAL_MEAN = 6.0
INTERARRIVAL_RATE = 1.0 / INTERARRIVAL_MEAN

AAM_SERVICE_TIME_MEAN = 5.0
AAM_SERVICE_TIME_RATE = 1.0 / AAM_SERVICE_TIME_MEAN

OPERATOR_1_SERVICE_TIME_MEAN = 12.0
OPERATOR_1_SERVICE_TIME_STDEV = 6.0

QUEUE_WAITING_TIME_LIMIT = 10.0

BREAK_TIME = 3
BREAK_TIME_RATE = 1/60.0

CUSTOMERS_SERVICED = 0

service_times_aam = []
service_times_operator_1 = []
service_times_operator_2 = []
queue_waiting_times_operator_1 = []
queue_waiting_times_operator_2 = []
unsatisfied_customers_incorrect_routed = []
unsatisfied_customers_overwaiting = []

#Arriving customers are initialized.
class Customer(object):
    def __init__(self, name, env, opr_num, sample_size, break_event):
        self.env = env
        self.name = name
        self.arrival_t = self.env.now
        self.action = env.process(self.call())
        self.opr_num = opr_num
        self.sample_size = sample_size
        self.break_event = break_event

    # Customers call automated answering mechanism.
    def call(self):
        global CUSTOMERS_SERVICED
        with automated_answer_mech.request() as req:
            # If the automated answer mechanism is full, the customer is dropped from the system.
            if automated_answer_mech.count == automated_answer_mech.capacity:
                return
            aam_service_duration = random.expovariate(AAM_SERVICE_TIME_RATE)
            yield self.env.timeout(aam_service_duration)
            automated_answer_mech.release(req)
            service_times_aam.append(aam_service_duration)

            # The misrouted customers with a probability of 0.1 are dropped.
            incorrect_routing_probability = random.uniform(0, 1)
            if incorrect_routing_probability < 0.1:
                unsatisfied_customers_incorrect_routed.append(self.name)
                return

            # Correctly routed customers are redirected into the operators.
            if self.opr_num == 1:
                yield self.env.process(self.call_operator_1())
            else:
                yield self.env.process(self.call_operator_2())

    # The customers that want to use operator 1 are connected.
    def call_operator_1(self):
        global CUSTOMERS_SERVICED
        queue_start_time = self.env.now
        with operator_1.request(priority = 0) as req:
            yield req | self.env.timeout(QUEUE_WAITING_TIME_LIMIT)
            # The customers that wait more than 10 minutes are dropped.
            if not req.triggered:
                queue_waiting_times_operator_1.append(QUEUE_WAITING_TIME_LIMIT)
                unsatisfied_customers_overwaiting.append(self.name)
                return

            queue_waiting_time = self.env.now - queue_start_time
            if queue_waiting_time != 0:
                queue_waiting_times_operator_1.append(queue_waiting_time)

            operator_1_service_duration = math.log(np.random.lognormal(OPERATOR_1_SERVICE_TIME_MEAN, OPERATOR_1_SERVICE_TIME_STDEV), math.e)
            while operator_1_service_duration < 0:
                operator_1_service_duration = math.log(np.random.lognormal(OPERATOR_1_SERVICE_TIME_MEAN, OPERATOR_1_SERVICE_TIME_STDEV), math.e)

            yield self.env.timeout(operator_1_service_duration)
            service_times_operator_1.append(operator_1_service_duration)
            CUSTOMERS_SERVICED += 1
            # If the customer serviced is the last customer, then the stopping event that terminates the simulation is triggered.
            if CUSTOMERS_SERVICED == self.sample_size:
                self.break_event.succeed()

    # The customers that want to use operator 2 are connected.
    def call_operator_2(self):
        global CUSTOMERS_SERVICED
        queue_start_time = self.env.now
        with operator_2.request(priority = 0) as req:
            yield req | self.env.timeout(QUEUE_WAITING_TIME_LIMIT)
            # The customers that wait more than 10 minutes are dropped.
            if not req.triggered:
                queue_waiting_times_operator_2.append(QUEUE_WAITING_TIME_LIMIT)
                unsatisfied_customers_overwaiting.append(self.name)
                return

            queue_waiting_time = self.env.now - queue_start_time
            if queue_waiting_time != 0:
                queue_waiting_times_operator_2.append(queue_waiting_time)

            operator_2_service_duration = random.uniform(1,7)
            yield self.env.timeout(operator_2_service_duration)
            service_times_operator_2.append(operator_2_service_duration)
            CUSTOMERS_SERVICED += 1
            # If the customer serviced is the last customer, then the stopping event that terminates the simulation is triggered.
            if CUSTOMERS_SERVICED == self.sample_size:
                self.break_event.succeed()


def customer_generator(env, sample_size, break_event):
    while True:
        yield env.timeout(random.expovariate(INTERARRIVAL_RATE))
        probability = random.uniform(0,1)
        opr_num = 1 if probability <= 0.3 else 2
        customer = Customer('Cust %s' %(i+1), env, opr_num, sample_size, break_event)


def break_call(env, operator):
    while True:
        yield env.timeout(np.random.poisson(BREAK_TIME_RATE))
        with operator.request(priority = 1) as req:
            yield req
            yield env.timeout(BREAK_TIME)


SEED_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
CUSTOMER_SIZE_LIST = [1000, 5000]

UTILIZATION_AAM_FINAL = [[], []]
UTILIZATION_OPERATOR_1_FINAL = [[], []]
UTILIZATION_OPERATOR_2_FINAL = [[], []]
AVERAGE_TOTAL_WAITING_TIME_FINAL = [[], []]
TOTAL_WAITING_TIME_TO_TOTAL_SYSTEM_TIME_FINAL = [[], []]
NUMBER_OF_WAITING_CUSTOMERS_OPERATOR_1_FINAL = [[], []]
NUMBER_OF_WAITING_CUSTOMERS_OPERATOR_2_FINAL = [[], []]
NUMBER_OF_UNSATISFIED_CUSTOMERS_FINAL = [[], []]


for seed in SEED_LIST:
    random.seed(seed)
    np.random.seed(seed)
    for (i, current_size) in enumerate(CUSTOMER_SIZE_LIST):
        CUSTOMERS_SERVICED = 0
        service_times_aam.clear()
        service_times_operator_1.clear()
        service_times_operator_2.clear()
        queue_waiting_times_operator_1.clear()
        queue_waiting_times_operator_2.clear()
        unsatisfied_customers_incorrect_routed.clear()
        unsatisfied_customers_overwaiting.clear()

        env = simpy.Environment()
        break_event = env.event()
        automated_answer_mech = simpy.Resource(env, capacity=100)
        operator_1 = simpy.PriorityResource(env, capacity=1)
        operator_2 = simpy.PriorityResource(env, capacity=1)
        env.process(customer_generator(env, current_size, break_event))
        env.process(break_call(env, operator_1))
        env.process(break_call(env, operator_2))
        env.run(until=break_event)
        system_time = env.now

        ###COLLECTING STATISTICS
        # UTILIZATION OF THE AAM
        utilization_aam = (sum(service_times_aam) / (100 * system_time))
        # UTILIZATION OF THE OPERATORS
        utilization_operator_1 = (sum(service_times_operator_1) / system_time)
        utilization_operator_2 = (sum(service_times_operator_2) / system_time)
        # AVERAGE TOTAL WAITING TIME
        total_waiting_time = sum(queue_waiting_times_operator_1) + sum(queue_waiting_times_operator_2)
        average_total_waiting_time = total_waiting_time / current_size
        # Maximum Total Waiting Time to Total System Time Ratio
        total_waiting_time_to_total_system_time = total_waiting_time / system_time
        #Number of waiting customers
        number_of_waiting_customers_operator_1 = len(queue_waiting_times_operator_1)
        number_of_waiting_customers_operator_2 = len(queue_waiting_times_operator_2)
        # Unsatisfied Customers
        number_of_unsatisfied_customers = len(unsatisfied_customers_overwaiting) + len(unsatisfied_customers_incorrect_routed)

        UTILIZATION_AAM_FINAL[i].append(utilization_aam)
        UTILIZATION_OPERATOR_1_FINAL[i].append(utilization_operator_1)
        UTILIZATION_OPERATOR_2_FINAL[i].append(utilization_operator_2)
        AVERAGE_TOTAL_WAITING_TIME_FINAL[i].append(average_total_waiting_time)
        TOTAL_WAITING_TIME_TO_TOTAL_SYSTEM_TIME_FINAL[i].append(total_waiting_time_to_total_system_time)
        NUMBER_OF_WAITING_CUSTOMERS_OPERATOR_1_FINAL[i].append(number_of_waiting_customers_operator_1)
        NUMBER_OF_WAITING_CUSTOMERS_OPERATOR_2_FINAL[i].append(number_of_waiting_customers_operator_2)
        NUMBER_OF_UNSATISFIED_CUSTOMERS_FINAL[i].append(number_of_unsatisfied_customers)

#FINAL STATISTICS:

#1.SAMPLE_SIZE = 1000

utilization_aam_1000 = np.average(UTILIZATION_AAM_FINAL[0])
utilization_operator_1_1000 = np.average(UTILIZATION_OPERATOR_1_FINAL[0])
utilization_operator_2_1000 = np.average(UTILIZATION_OPERATOR_2_FINAL[0])
average_total_waiting_time_1000 = np.average(AVERAGE_TOTAL_WAITING_TIME_FINAL[0])
total_waiting_time_to_total_system_time_1000 = np.max(TOTAL_WAITING_TIME_TO_TOTAL_SYSTEM_TIME_FINAL[0])
average_number_of_waiting_customers_operator_1_1000 = np.average(NUMBER_OF_WAITING_CUSTOMERS_OPERATOR_1_FINAL[0])
average_number_of_waiting_customers_operator_2_1000 = np.average(NUMBER_OF_WAITING_CUSTOMERS_OPERATOR_2_FINAL[0])
average_number_of_unsatisfied_customers_1000 = np.average(NUMBER_OF_UNSATISFIED_CUSTOMERS_FINAL[0])

#2.SAMPLE_SIZE = 5000

utilization_aam_5000 = np.average(UTILIZATION_AAM_FINAL[1])
utilization_operator_1_5000 = np.average(UTILIZATION_OPERATOR_1_FINAL[1])
utilization_operator_2_5000 = np.average(UTILIZATION_OPERATOR_2_FINAL[1])
average_total_waiting_time_5000 = np.average(AVERAGE_TOTAL_WAITING_TIME_FINAL[1])
total_waiting_time_to_total_system_time_5000 = np.average(TOTAL_WAITING_TIME_TO_TOTAL_SYSTEM_TIME_FINAL[1])
average_number_of_waiting_customers_operator_1_5000 = np.average(NUMBER_OF_WAITING_CUSTOMERS_OPERATOR_1_FINAL[1])
average_number_of_waiting_customers_operator_2_5000 = np.average(NUMBER_OF_WAITING_CUSTOMERS_OPERATOR_2_FINAL[1])
average_number_of_unsatisfied_customers_5000 = np.average(NUMBER_OF_UNSATISFIED_CUSTOMERS_FINAL[1])

print('Simulation of the System for 1000 Customers:')
print("Utillization of Answering System: ",utilization_aam_1000)
print("Utillization of Operator 1: ",utilization_operator_1_1000)
print("Utillization of Operator 2: ",utilization_operator_2_1000)
print("Average Total Waiting Time: ",average_total_waiting_time_1000)
print("Maximum Total Waiting Time to Total System Time Ratio: ",total_waiting_time_to_total_system_time_1000)
print("Average Number of People Waiting to be Served by Operator 1: ",average_number_of_waiting_customers_operator_1_1000)
print("Average Number of People Waiting to be Served by Operator 2: ",average_number_of_waiting_customers_operator_2_1000)
print("Average Number of Unsatistied Customers: ",average_number_of_unsatisfied_customers_1000,"\n")

print('Simulation of the System for 5000 Customers:')
print("Utillization of Answering System:",utilization_aam_5000)
print("Utillization of Operator 1: ",utilization_operator_1_5000)
print("Utillization of Operator 2: ",utilization_operator_2_5000)
print("Average Total Waiting Time: ",average_total_waiting_time_5000)
print("Maximum Total Waiting Time to Total System Time Ratio: ",total_waiting_time_to_total_system_time_5000)
print("Average Number of People Waiting to be Served by Operator 1: ",average_number_of_waiting_customers_operator_1_5000)
print("Average Number of People Waiting to be Served by Operator 2: ",average_number_of_waiting_customers_operator_2_5000)
print("Average Number of Unsatistied Customers: ",average_number_of_unsatisfied_customers_5000)
