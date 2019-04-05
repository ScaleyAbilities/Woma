using System;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace Woma
{
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

            var lines = File.ReadAllLines(filename);

            Console.WriteLine("Inserting Records...");

            var tasks = new Task[Instances];

            var inserted = new int[Instances];

            for (var i = 0; i < Instances; i++)
            {
                var instance = i; // Fixes closure issues
                tasks[instance] = Task.Run(() => {
                    var instanceLines = lines.Where(l => l[l.IndexOf(',') + 1] % Instances == instance);

                    foreach (var line in instanceLines.Select(l => l.Trim()))
                    {
                        var firstComma = line.IndexOf(',');
                        var start = line.IndexOf(' ') + 1;
                        var command = line.Substring(start, firstComma - start);
                        var commandParams = line.Substring(firstComma + 1).Split(',');
                        
                        if (commandParams.Length < 1) {
                            Console.WriteLine("Bad line" + line);
                        }

                        var json = new JObject();
                        json.Add("cmd", command);

                        var jsonParams = new JObject();

                        if (commandParams.Length > 0)
                        {
                            if (command == "DUMPLOG" && commandParams.Length == 1)
                                jsonParams.Add("filename", commandParams[0]);
                            else
                                json.Add("usr", commandParams[0]);
                        }

                        if (commandParams.Length > 1)
                        {
                            if (command == "ADD")
                                jsonParams.Add("amount", commandParams[1]);
                            else if (command == "DUMPLOG")
                                jsonParams.Add("filename", commandParams[1]);
                            else
                                jsonParams.Add("stock", commandParams[1]);
                        }

                        if (commandParams.Length > 2)
                        {
                            if (command == "SET_BUY_TRIGGER" || command == "SET_SELL_TRIGGER")
                                jsonParams.Add("price", commandParams[2]);
                            else
                                jsonParams.Add("amount", commandParams[2]);
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
