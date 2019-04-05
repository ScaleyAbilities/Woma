using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace Woma
{
    class Command
    {
        public string Name;
        public string Username;
        public string[] Params;
    }

    class Program
    {
        internal static int Instances = int.Parse(Environment.GetEnvironmentVariable("INSTANCES") ?? "1");
        internal static string Filename = Environment.GetEnvironmentVariable("WORKLOAD_FILE");

        static void Main(string[] args)
        {
            if (args.Length < 1 && Filename == null)
            {
                Console.WriteLine("No file specified.");
                Environment.Exit(1);
            }

            var filename = Filename ?? args[0];
            if (!File.Exists(filename))
            {
                Console.WriteLine("File doesn't exist.");
                Environment.Exit(1);
            }

            Console.WriteLine("Loading Records...");

            var commands = File.ReadAllLines(filename).Select(line => {
                var command = new Command();
                var firstComma = line.IndexOf(',');
                var start = line.IndexOf(' ') + 1;
                command.Name = line.Substring(start, firstComma - start).Trim();
                command.Params = line.Substring(firstComma + 1).Split(',').Select(p => p.Trim()).ToArray();

                if (command.Name != "DUMPLOG" || command.Params.Length > 1)
                    command.Username = command.Params[0];

                return command;
            });

            var usernames = new HashSet<string>();
            foreach (var command in commands)
            {
                if (command.Username != null)
                    usernames.Add(command.Username);
            }

            var usernameQueue = new Queue<string>(usernames);
            var groupedUsernames = new HashSet<string>[Instances];
            var index = 0;
            while (usernameQueue.Any())
            {
                var username = usernameQueue.Dequeue();

                if (groupedUsernames[index] == null)
                    groupedUsernames[index] = new HashSet<string>();

                groupedUsernames[index].Add(username);
                index = (index + 1) % Instances;
            }

            var groupedCommands = new IEnumerable<Command>[Instances];
            for (var i = 0; i < Instances; i++)
            {
                var localI = i;
                groupedCommands[localI] = commands.Where(c => c.Username != null && groupedUsernames[localI].Contains(c.Username));
            }

            // Add any null usernames to the final group
            groupedCommands[Instances - 1] = groupedCommands[Instances - 1].Concat(commands.Where(c => c.Username == null));

            Console.WriteLine($"Loaded {usernames.Count()} usernames");
            
            Console.WriteLine("Inserting Records...");

            var tasks = new Task[Instances];
            var inserted = new int[Instances];

            for (var i = 0; i < Instances; i++)
            {
                var instance = i; // Fixes closure issues
                tasks[instance] = Task.Run(() => {
                    foreach (var command in groupedCommands[instance])
                    {                        
                        var json = new JObject();
                        json.Add("cmd", command.Name);
                        json.Add("usr", command.Username);

                        var jsonParams = new JObject();

                        if (command.Name == "DUMPLOG" && command.Params.Length == 1)
                            jsonParams.Add("filename", command.Params[0]);

                        if (command.Params.Length > 1)
                        {
                            if (command.Name == "ADD")
                                jsonParams.Add("amount", command.Params[1]);
                            else if (command.Name == "DUMPLOG")
                                jsonParams.Add("filename", command.Params[1]);
                            else
                                jsonParams.Add("stock", command.Params[1]);
                        }

                        if (command.Params.Length > 2)
                        {
                            if (command.Name == "SET_BUY_TRIGGER" || command.Name == "SET_SELL_TRIGGER")
                                jsonParams.Add("price", command.Params[2]);
                            else
                                jsonParams.Add("amount", command.Params[2]);
                        }

                        json.Add("params", jsonParams);

                        RabbitHelper.PushCommand(json, instance + 1);
                        Interlocked.Increment(ref inserted[instance]);
                    }
                });
            }

            var waitTask = Task.WhenAll(tasks);

            while (!waitTask.IsCompleted)
            {
                Task.WaitAny(waitTask, Task.Delay(5000));

                Console.WriteLine("");
                for (var i = 0; i < Instances; i++)
                {
                    Console.WriteLine($"Commands {i + 1}: {inserted[i]} entries");
                }
            }
            
            Console.WriteLine("Done.");
            Environment.Exit(0);
        }
    }
}
